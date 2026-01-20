import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx


def heavy_computation(n):
    return sum(i * i for i in range(n))


async def fetch_url(client, url, semaphore):
    async with semaphore:
        response = await client.get(url)
        return len(response.content)


async def run_async_fetcher(urls):
    semaphore = asyncio.Semaphore(5)  # Máximo 5 tareas concurrentes
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)


# 3. Comparación Síncrona
def run_sync_fetcher(urls):
    with httpx.Client() as client:
        return [len(client.get(url).content) for url in urls]


if __name__ == "__main__":
    urls = ["https://www.google.com"] * 20

    # Medir Síncrono
    start = time.perf_counter()
    run_sync_fetcher(urls)
    print(f"Síncrono: {time.perf_counter() - start:.2f}s")

    # Medir Asíncrono
    start = time.perf_counter()
    asyncio.run(run_async_fetcher(urls))
    print(f"Asíncrono (asyncio): {time.perf_counter() - start:.2f}s")

    # Medir CPU-Bound con Procesos
    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        list(executor.map(heavy_computation, [10**7] * 4))
    print(f"CPU-bound (Multiprocessing): {time.perf_counter() - start:.2f}s")

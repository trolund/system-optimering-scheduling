#https://www.folkstalk.com/tech/threadpool-python-map-with-code-examples/
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
values = [2,3,4,5]
def square(n):
   return n * n
with ThreadPoolExecutor(max_workers = 4) as executor:
    results = executor.map(square, values)
    for result in as_completed(results):
        print(result)

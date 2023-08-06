# SPACESHIP RENTAL API
> Spaceship rental API with high profitability

Optimize the profitability of your rental company by selecting the contracts that will maximize your income.
* A simple-to-use API
* Based on Python 3.10 and FastAPI

## Installation
Install dependencies with
```sh
pip install -r ./setup/requirements.txt
```

## Usage
In production, run your application with
```sh
uvicorn main:app --port 8080
```
### Input example
```json
[
    {"name": "Contract1", "start": 0, "duration": 5, "price": 10},
    {"name": "Contract2", "start": 3, "duration": 7, "price": 14},
    {"name": "Contract3", "start": 5, "duration": 9, "price": 8},
    {"name": "Contract4", "start": 5, "duration": 9, "price": 7}
]
```
### Output example
```json
{
    "income": 18,
    "path": ["Contract1", "Contract3"]
}
```

## Development setup
Install additional dependencies for testing & profiling with
```sh
pip install -r ./setup/requirements-dev-extra.txt
```

During development, run your application with
```sh
uvicorn main:app --port 8080 --reload
```

You can then test directly on
```
http://127.0.0.1:8080/docs
```
### Quality check
Format your python code with
```sh
black .
```
Check your type annotations with
```sh
mypy . --config-file ./setup/mypy.ini
```

### Unit tests
Run the automated test suite with
```sh
python -m unittest discover -s ./test/
```

## Performance
Metrics below have been measured with `timeit` and `memory_profiler` on the main algorithm (not on the global api).

| Contracts number  | Execution time  | Memory usage  |
| ----------------- | --------------- | --------------|
| 10                | 20us            | 23.4MB        |
| 100               | 0.2ms           | 23.4MB        |
| 1000              | 2ms             | 23.8MB        |
| 10000             | 40ms            | 28.4MB        |
| 20000             | 80ms            | 33.5MB        |
| 50000             | 0.2s            | 48.6MB        |
| 100000            | 0.5s            | 73.9MB        |
| 500000            | 4s              | 271.6MB       |

## Release History
* 0.2.0
    * Improved contract optimizer with binary search to find the nearest successor
    * Added mypy for type annotations checking
    * Added black for code formatting
* 0.1.0
    * Improved contract optimizer: when building path of successors, stop at 2nd successor
    * Optimized function calls with cProfile
    * Added profiling for execution time and memory usage
    * Added contract generator for testing
    * Added missing docstrings
* 0.0.1
    * Initialized API for contract optimizer
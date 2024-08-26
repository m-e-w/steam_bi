# Change Log
## Version: 1.01.00
- Officially deprecated the legacy python code and moved it to a dedicated repos: https://github.com/m-e-w/steam_bi_legacy
- Added support for asynchronous task/job (worker) based execution
    - Instead of running a python script, there is now a WSGI HTTP Server and asynchronous task queue that tasks can be sent to and monitored from using an API
    - This change adds a lot of versatility / robustness to the project as now tasks can be queued and monitored via HTTP requests as opposed to manually running a python script
- Substantial project restructure and documentation overhaul
- Added bash scripts to help automate project setup / testing
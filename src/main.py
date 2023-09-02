import uvicorn

def main(port: int, host: str, reload: bool):

    options = {
        'reload': reload,
    }
    options['port'] = port
    options['host'] = host
    
    # # Configure log level for uvicorn
    # if verbose:
    #     lv = max(verbose, len(LOG_LEVELS.keys()))
    #     options['log_level'] = LOG_LEVELS[lv]
    # else:
    #     options['log_level'] = 'warning'
    uvicorn.run('src.app:app', **options)


if __name__ == '__main__':
    main(5000, "0.0.0.0", True)

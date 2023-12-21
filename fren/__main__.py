if __name__ == "__main__":
    from fren.logger import setup_logging
    setup_logging()

    try: #TODO this is only for testing, really
        from fren.app import main
        main()
    except KeyboardInterrupt:
        print("\nQUITTING!!!")
        exit(0)

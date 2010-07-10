class UI:
    def __init__(self, engine, numPlayers):
        self.engine = engine
        self.numPlayers = numPlayers

    def start(self):
        self.engine.run()

    def status(self, status):
        print(status)

    def prompt(self, options):
        choice = input("Choose: " + 
            ", ".join(list(options.keys())) + "? ")
        if choice in options:
            options[choice]()
        else:
            print("Bad option")

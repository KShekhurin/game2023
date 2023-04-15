from App import App
from Frames import LogoFrame, MenuFrame


def main():
    frame = MenuFrame()
    application = App(frame, (1000, 750))
    application.start()


if __name__ == '__main__':
    main()

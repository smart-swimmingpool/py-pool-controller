import mip

class Installer:
    
    def install_deps(self): 
        try:
            mip.install("logging")
            # mip.install("https://github.com/george-hawkins/micropython-wifi-setup")
            # mip.install("github:stritti/micropython-wifi-setup", version="feature/add-mip-capabilities")

        except Exception as e:
            # printing stack trace
            import sys
            sys.print_exception(e) 


if __name__ == "__main__":
    inst = Installer()
    inst.install_deps()

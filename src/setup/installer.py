import mip

class Installer:
    
    def install_deps(self): 
        try:
            mip.install("logging")

        except Exception as e:
            # printing stack trace
            import sys
            sys.print_exception(e) 

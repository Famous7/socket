import threading
import time

def func(value, count):
	while count > 0:
		print("{0} : in {1}".format(value, threading.get_ident()))
		time.sleep(1)
		count -= 1
        

if __name__ == "__main__":
	t1 = threading.Thread(target=func, args=("Daemon", 5))
	t2 = threading.Thread(target=func, args=("Non-Daemon", 2))
	t1.daemon=True
	t1.start()
	t2.start()

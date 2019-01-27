import sys, requests
from multiprocessing import Pool
from termcolor import colored

if len(sys.argv) != 2:
	print("Usage: python3 {} <path to file>".format(sys.argv[0]))
	exit(1)


def check_url(url):
	if not (url.startswith('https://') or url.startswith('http://')):
		url='http://'+url
	
	url = url.rstrip()
	if url.endswith('/'):
		url+='.git'
	else:
		url+='/.git'
	#print(url)	
	try:
		r=requests.get(url, timeout=10)
		if str(r.status_code)=='200' and ".git" in r.url:
			print(colored("Found .git dir on " + url + " ---->>> " + str(r.status_code),'green'))
	except:
		print(colored("Timeout ("+url+")",'red'))


if __name__ == '__main__':
	file=sys.argv[1]
	print("Reading from file : "+file)
	urls = [line.rstrip() for line in open(file)]
	#print(urls)
	pool = Pool(processes=32)
	try: pool.map_async(check_url, urls).get(2**32)
	except KeyboardInterrupt: pass
from flask import Flask, render_template, request
import numpy as np
from scipy.sparse.linalg import eigs
import os
import time
import glob
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import shutil



file_db = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/hello', methods=['POST'])
def hello():
	
	first_name = request.form['first_name']
	search = first_name
	val = op(search)
	return first_name



def op(pink):
	for filepath in glob.glob('Pages/Temp/*.html'):
		f = open(filepath, "r")
		for line in f:
		    if fuzz.WRatio(pink, line) > 76:
		        shutil.copy(filepath, 'Pages/') 
		        file_db.append(int(filepath[15:16]))
		        flag =1
		        break
		    else:
		        flag = 0

	print(file_db)
	    
	def main():    
	    # Figure out how many files there are to read, construct matrix with that size
	    count = (int(os.popen("ls Pages/| wc -l").read().strip()))
	    print(count)
	    matrix = [x[:] for x in [[0]*count]*count]

	    # Parse the text files and populate matrix with data from Parser
	    parserOutput = os.popen("./parser.sh").read().split()
	    i = 0
	    while i < len(parserOutput):
	    	try:
	    		matrix[int(parserOutput[i])][int(parserOutput[i+1])] = float(parserOutput[i+2])
	    		i += 3
	    	except IndexError:
	    		i+=3
        
	        
	    # Output Data while calculating the Eigenvectors
	    print("Constructed Matrix:\n" + str(np.matrix(matrix)) + "\n\n")
	    vals, vecs = eigs(np.array(matrix), k=1)
	    print("Eigenvalues:\n" + str(np.matrix(vals)) + "\n\n")
	    print("Eigenvectors:\n"+ str(np.matrix(vecs)) + "\n\n")

	    # Discard Complex variables
	    eigenvector = []
	    for vec in vecs:
	        eigenvector.append(float(vec[0]))

	    # Print Search Results
	    print("\nSearch Results:")
	    for page in np.argsort(eigenvector)[::-1]:
	    	if (page+1) in file_db:
	    		print("Page " + str(page+1))

	start_time = time.time()
	main()
	print("--- %s seconds ---" % (time.time() - start_time))

	files = glob.glob('Pages/*.html')
	for f in files:
		os.remove(f)

if __name__ == '__main__':
    app.run(debug=True)
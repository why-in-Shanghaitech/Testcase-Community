import os
import subprocess
import time

# fit the environment
time_limit = 0.1        # default time limit is 0.1 s
pre = ""
python_version = "python3"
if os.name=='nt':
    # if it is under windows
    pre = "./"
    python_version = "python"
    time_limit = 1      # default time limit on windows is 1 s
elif os.name=='posix':
	# if it is under linux
    pass

# update testcases
if not(os.path.exists(pre + ".git")):
    os.system("git init")
    os.system("git remote add -f origin https://github.com/why-in-Shanghaitech/Testcase-Community.git")
    os.system("git config core.sparsecheckout true")
    os.system("echo testcase >> .git/info/sparse-checkout")
os.system("git fetch --all && git reset --hard origin/master")

# initilize varibles
i = 1
case = []
ac_case, wa_case, re_case, tle_case = 0, 0, 0, 0
st_dict = {'ac ':'Accept',
            'wa ':'Wrong Answer',
            're ':'Run Time Error',
            'tle':'Time Limit Exceeded'}

# check the input file
if not(os.path.exists(pre + "hw6.py")):
    pass

while True:
    # check the input file
    if not(os.path.exists(pre +"testcase/"+str(i)+".in")):
        break

    # run the program
    myanswer = subprocess.Popen(python_version + " hw6.py <" + pre + "testcase/"+str(i)+".in", stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True) 
    t_beginning = time.time() 
    seconds_passed = 0 
    while True: 
        # if the program terminates
        if myanswer.poll() is not None:
            seconds_passed = time.time() - t_beginning 

            # get the answer
            cur_answer = myanswer.stdout.read().decode('utf-8')

            # check run time error (not very meticulous)
            if cur_answer[:9]=="Traceback":
                case.append(('re ',seconds_passed))
                re_case += 1
            else:
                # check if it is the right answer
                answer = open( pre + "testcase/"+str(i)+".out", "r+")
                if cur_answer == answer.readline():
                    case.append(('ac ',seconds_passed))
                    ac_case += 1
                else:
                    case.append(('wa ',seconds_passed))
                    wa_case += 1
                answer.close()
            break 
        
        # judge time limit exceeded
        seconds_passed = time.time() - t_beginning 
        if time_limit and seconds_passed > time_limit: 
            myanswer.terminate() 
            case.append(('tle',seconds_passed))
            tle_case += 1
            break
    i += 1

	

# print the report
print("\n\n\n\n========= Below is your report =========")
print("    ID           Status         Time\n")
for i in range(len(case)):
    print("   {0:3}     {1:^19}  {2:.2f}ms".format(i+1,st_dict[case[i][0]],1000*case[i][1]))
print("\n=========== The final result ===========")
print("          Status            Numbers\n")
static = [ac_case, wa_case, re_case, tle_case]
status = ['ac ','wa ','re ','tle']
for i in range(4):
    print("    {0:^19}       {1:^3}".format(st_dict[status[i]],static[i]))
print("----------------------------------------")
print("    {0:^19}       {1:^3}".format('Total',sum(static)))

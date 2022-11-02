import sys
import copy

#non-preemptive SJF - Shortest Job First
#SRTF Shortest Remaining Time First
#RR - Round Robin, quantum=3


#initialization function, opens file from the argument and populates the list of processes
def initialize(p):
	if len(sys.argv)>2:
		print("Too many arguments\n")
		sys.exit()
	elif len(sys.argv)==1:
		print("No file provided")
	else:
		FILE = open(sys.argv[1],'r')
		while True:
			line=FILE.readline()
			line.strip('\n')
			if line != '':
				line=line.split(' ')
				new = process(line[0],line[1],line[2])
				p.append(new)
			else:
				break

#class process to operate with OOP
class process:
	def __init__(self,name,burst,arrival):
		self.name=name
		self.burst=int(burst)
		self.arrival=int(arrival)

#helping function to calculate and print stats
#takes in stats list present in every function, original process list and the letter to print stats for
def print_stats(s,p,l):
	for i in range(len(s)):
		if s[i].name==l:
			for j in range(len(p)):
				if p[j].name==l:
					print(l,'		',s[i].burst,'		',s[i].burst-p[j].burst)

#implementation of SJF
def SJF(p):
	#copy the original array to manipulate data freely without losing the original
	#some initializations for future use
	proc=copy.deepcopy(p)
	stats=[]
	timer=0
	print("SJF Scheduling")
	current=process('',0,0)
	
	
	#while we still have a list or there is a process in execution
	while proc or current.burst>0:
		#if current process is over and there is an available process - find the one with minimal burst time
		if current.burst==0 and proc[0].arrival==0:
			minimum,pid=proc[0].burst,0
			for i in range(len(proc)):
				if proc[i].burst < minimum and proc[i].arrival==0:
					minimum=proc[i].burst
					pid=i
				#check for alphabet requirement
				#picks the alphabetically first letter if they have equal burst times
				elif proc[i].burst==minimum and proc[i].arrival==0:
					if proc[i].name<proc[pid].name:
						minimum=proc[i].burst
						pid=i
			
			#plug in the new process for execution	
			current.name=proc[pid].name
			current.burst=proc[pid].burst
			current.arrival=proc[pid].arrival
			
			print(timer,current.name, end=' ')
			del proc[pid]
		
		#increments of timer to simulate execution of the process and control arriving processes
		current.burst=current.burst-1
		for i in range(len(proc)):
			if proc[i].arrival>0:
				proc[i].arrival-=1	
		timer+=1
		
		if current.burst == 0:
			temp = process(current.name,timer,0)
			stats.append(temp)
			print("Process terminated")
	
	#printing table	
	print(timer, "complete")
	print('\n\n')
	print('Process ID |','Turnaround Time |','Waiting Time')
	print_stats(stats,p,'A')
	print_stats(stats,p,'B')
	print_stats(stats,p,'C')
	print_stats(stats,p,'D')
	print_stats(stats,p,'E')
	print_stats(stats,p,'F')
	print_stats(stats,p,'G')
	print_stats(stats,p,'H')
	print('\n\n')

def SRTF(p):
	#copy the original array to manipulate data freely without losing the original
	#some initializations for future use
	proc=copy.deepcopy(p)
	timer=0
	stats=[]
	minimum,pid=100,0
	flag=0
	print("\nSRTF Scheduling")
	current=process(proc[0].name,proc[0].burst,proc[0].arrival)
	del proc[0]
	
	#checking if there are any available processes
	#in case we don't have any processes original and we are waiting for their arrival
	if current.arrival > 0:
		for i in range(len(proc)):
			if proc[i].burst < minimum and proc[i].arrival==0:
					minimum=proc[i].burst
					pid=i
			elif proc[i].burst==minimum and proc[i].arrival==0:
					if proc[i].name<proc[pid].name:
						minimum=proc[i].burst
						pid=i
		if minimum==100:
			timer+=1
		else:
			temp=process(current.name,current.burst,current.arrival)
			proc.append()
			current.name=proc[pid].name
			current.burst=proc[pid].burst
			current.arrival=proc[pid].arrival
			del proc[pid]
	
	print(timer,current.name,end=" ")
	
	
	#while we still have a list or there is a process in execution
	while proc or current.burst>0:
		#if the previous process is done, we must find the shortest replacement
		#flag 2 indicates that the process is done and we do not need to switch it back to ready queue
		if current.burst==0:
			minimum,pid=100,0
			for i in range(len(proc)):
				if proc[i].burst < minimum and proc[i].arrival==0:
					minimum=proc[i].burst
					pid=i
					flag=2
				elif proc[i].burst==minimum and proc[i].arrival==0:
					if proc[i].name<proc[pid].name:
						minimum=proc[i].burst
						pid=i
						
		#general check for potential preemptive swap
		#flag 1 indicates that we have found the replacement but the previous process is not done
		#and we have to swap it back to ready queue
		else:
			minimum,pid=100,0
			for i in range(len(proc)):
				if proc[i].burst < current.burst and proc[i].arrival==0:
					minimum=proc[i].burst
					pid=i
					flag=1
				elif proc[i].burst==minimum and proc[i].arrival==0:
					if proc[i].name<proc[pid].name:
						minimum=proc[i].burst
						pid=i
				
		#preemptive swap of current process back into ready queue and previously found replacement	
		if flag==1:
			print("Process preempted by process with shorter burst time")
			temp=process(current.name,current.burst,current.arrival)
			proc.append(temp)
			current.name=proc[pid].name
			current.burst=proc[pid].burst
			current.arrival=proc[pid].arrival
			del proc[pid]
			flag=0
			print(timer,current.name,end=" ")
		#just selecting new process without a swap since the process has ended
		elif flag==2:
			current.name=proc[pid].name
			current.burst=proc[pid].burst
			current.arrival=proc[pid].arrival
			del proc[pid]
			flag=0
			print(timer,current.name,end=" ")
			
		
		#increments	
		current.burst=current.burst-1
		for i in range(len(proc)):
			if proc[i].arrival>0:
				proc[i].arrival-=1	
		timer+=1
		
		if current.burst==0:
			temp = process(current.name,timer,0)
			stats.append(temp)
			print("Process terminated")
			
	#printing table
	print(timer, "complete")
	print('\n\n')
	print('Process ID |','Turnaround Time |','Waiting Time')
	print_stats(stats,p,'A')
	print_stats(stats,p,'B')
	print_stats(stats,p,'C')
	print_stats(stats,p,'D')
	print_stats(stats,p,'E')
	print_stats(stats,p,'F')
	print_stats(stats,p,'G')
	print_stats(stats,p,'H')
	print('\n\n')

def RR(p,q):
	#copy the original array to manipulate data freely without losing the original
	#some initializations for future use
	#the algorithm works on pointer principle and we are just modifying the data according to pointer
	proc=copy.deepcopy(p)
	timer=0
	c_q = 0
	pointer=0
	stats=[]
	print("\nRR Scheduling")
	#selecting the very first process upon arrival
	current=process(proc[pointer].name,proc[pointer].burst,proc[pointer].arrival)
	print(timer,current.name, end=" ")
	
	#while we still have a list or there is a process in execution
	while proc or current.burst>0:
		
		#if the process has ended we must get rid of its copy in ready queue
		if current.burst==0:
			temp = process(current.name,timer,0)
			stats.append(temp)
			print("Process terminated")
			del proc[pointer]
			#if there is no list - we're done
			if not proc:
				print(timer, "complete")
				print('\n\n')
				print('Process ID |','Turnaround Time |','Waiting Time')
				print_stats(stats,p,'A')
				print_stats(stats,p,'B')
				print_stats(stats,p,'C')
				print_stats(stats,p,'D')
				print_stats(stats,p,'E')
				print_stats(stats,p,'F')
				print_stats(stats,p,'G')
				print_stats(stats,p,'H')
				print('\n\n')
				break
			#if we deleted an item that happened to be last - we return to the beginning of the ready queue
			elif pointer==len(proc):
				pointer=0
			#if we reached a process that has not arrived yet - we return to the beginning
			#(we can do so because we practically have a sorted list and there are no valid entries after)
			elif proc[pointer].arrival!=0:
				pointer=0
			current.name=proc[pointer].name
			current.burst=proc[pointer].burst
			current.arrival=proc[pointer].arrival
			c_q=0
			print(timer,current.name, end=" ")
			
		#if we reached the limit - we go to the next item in queue	
		elif c_q == q:
			print("Quantum expired")
			proc[pointer].burst = current.burst
			
			#if we deleted an item that happened to be last - we return to the beginning of the ready queue
			if pointer+1==len(proc):
				pointer=0
			#if the next item already arrived - we work with it
			elif proc[pointer+1].arrival==0:
				pointer+=1
			#if not, then we reached not yet arrived processes and we must return to the beginning
			else:
				pointer=0
				
			current.name=proc[pointer].name
			current.burst=proc[pointer].burst
			current.arrival=proc[pointer].arrival
			c_q=0
			print(timer,current.name, end=" ")
			
#		print("current:",current.name,current.burst,current.arrival)
#		for i in range(len(proc)):	
#			print("in proc: ",proc[i].name,proc[i].burst,proc[i].arrival)	
#		print("\n\n")
	
		current.burst=current.burst-1
		for i in range(len(proc)):
			if proc[i].arrival>0:
				proc[i].arrival-=1	
		timer+=1
		c_q+=1

def main():
	orig_p=[]
	initialize(orig_p)
	SJF(orig_p)
	SRTF(orig_p)
	RR(orig_p,3)
	
	

main()

#@title Default title text
# simulation
# 1 : up
# 2 : left
# 3 : down
# 4 : right
import numpy as np
import random
import time
import matplotlib
import matplotlib.pyplot as plt
 
SIZE_L = 30
SIZE_B = 30
 
en = np.zeros((SIZE_L,SIZE_B))
#print(en)
class Person:
    def __init__(self,env,x=None,y=None,):
      
      self.x = x
      self.y = y
      self.subject_sign=1
      self.contact=False
      self.immune = False
      self.env=env
      self.env[x][y]=self.subject_sign
      self.treatment_step=0
      self.medicines=5
      self.current_step = 0
      self.treatment=False
      self.income=0
      self.prev_post=None
      self.earning = 0.001
      self.infected_times = 0
      self.infected_days = None
      self.infection_period = 20
      self.death=False
      # print(self.env)
    def step_update(self,step):
      self.current_step=step
      if self.treatment is True:
        
        if self.current_step > self.treatment_step:
          self.contact = False
          self.treatment=False
 
    def move(self,direct,infected=None,contagion=False):
      prev_state=self.contact
      if direct == 1:   #up
        if self.x<=0:
          self.env[self.x][self.y]=self.subject_sign
        else:
          self.env[self.x-1][self.y]=self.subject_sign
          self.env[self.x][self.y]=0
          self.x=self.x-1
 
      elif direct == 2:   # left
        if self.y<=0:
          self.env[self.x][self.y]=self.subject_sign
        else:
          self.env[self.x][self.y-1]=self.subject_sign
          self.env[self.x][self.y]=0
          self.y=self.y-1
 
      elif direct == 3:   #down
        if self.x>=(SIZE_B-1):
          self.env[self.x][self.y]=self.subject_sign
        else:
          self.env[self.x+1][self.y]=self.subject_sign
          self.env[self.x][self.y]=0
          self.x=self.x+1
      
      elif direct == 4:   #right
        if self.y>=(SIZE_L-1):
          self.env[self.x][self.y]=self.subject_sign
        else:
          self.env[self.x][self.y+1]=self.subject_sign
          self.env[self.x][self.y]=0
          self.y=self.y+1
      
      elif direct == 5: #No MOvement
        pass
      duplicate = []
      #print(posi)
      #if (self.x,self.y) in posi:posi.remove((self.x,self.y))
      for a in infected:
        if a == (self.x,self.y):
          duplicate.append(a)
      self.contagion=contagion
             
      if self.contact==False and contagion==True and len(duplicate)>=1 and self.immune==False and self.treatment is False: #steps to contact
        self.contact = True
        self.subject_sign='4'
        
        
        #print("posi--",posi,"Duplicate : ",duplicate,"\n\n")   
        #print("Virus}|}}{{}{{}}{}{{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{{}{}{}{}{}{}{}{}{}")
 
      
 
      if self.contact==True and prev_state==False:
        #if self.contact:print(self.infected_days,self.current_step)
        self.infected_days = self.current_step+self.infection_period
        self.infected_times=self.infected_times+1
 
      if self.infected_days!=None and self.contact == True and self.current_step>self.infected_days:
       # print(self.infected_days)
        self.contact=False
        #print('Self Treatment')
        self.infected=None
        if random.random() < 1/10000:
          self.death=True
      return self.env,self.x,self.y,self.contact
 
    def vacinated(self,x1=8,x2=12,y1=8,y2=12):
      if self.x>= x1 and self.x<= x2 and self.y>= y1 and self.y<= y2:
              self.contact = False
              self.immune = True
              self.subject_sign='7'
      return self.immune
 
    def hospital(self,x1,x2,y1,y2):
      if self.x>= x1 and self.x<= x2 and self.y>= y1 and self.y<= y2:
        if self.immune==False and self.contact==True and self.treatment == False :
           self.subject_sign=3
           self.treatment=True
           self.treatment_step=self.current_step+self.medicines
           #print("Treatment..............................\t\t\t\t\t\t.........")
           
    def Earning(self):
      if ((self.x,self.y) is not self.prev_post) and self.contact==False and self.contagion==False:
        self.income = self.income + self.earning
 
      elif ((self.x,self.y) is not self.prev_post) and self.contact==True:
        self.income = self.income - (self.earning*2)
      
      elif ((self.x,self.y) is not self.prev_post) and self.contact==False and self.contagion==True:
        self.income = self.income + (self.earning*8/10)
 
      return self.income
 
    def Death(self,):
      '''if random.random() < self.infected_times/100000:
        self.death=True'''
 
      if random.randrange(0,20000)<=self.infected_times and self.contact:
        self.death=True
      return self.death
    
"""
def step(psn=None,posts=None):
    ipt = random.randint(1,4)
    if ipt == 1:
       env,x,y,state=psn.move(1,posts)
    elif ipt == 2:
      env,x,y,state= psn.move(2,posts)
    elif ipt == 3:
      env,x,y,state=psn.move(3,posts)
    elif ipt == 4:
      env,x,y,state= psn.move(4,posts)
    return env,x,y,state"""
    
 
class simulation_control:
  def __init__(self,NOP=None,env=None):
    self.NOP=NOP
    self.en=env
    self.immune_code = 2
    self.hospital_code = 5
    self.contact = 0
    self.contact_list = []
    self.vacinated = []
    self.steps=[]
    self.immune_steps = []
    self.prev_contacts = 0
    self.cnt=[]
    self.total_recovered=[]
    self.immune=[]
    self.prev_immune=0
    self.infected=[]
    self.current_step = 1
    self.new_case_list=[]
    self.recovery_list=[]
    self.new_case_steps=[]
    self.recovery_steps=[]
    self.total_recovered_cases=0
    self.Total_Economy_perstep = 0
    self.Total_income_list=[]
    self.current_step_lst=[]
    self.lockdown_percent = 0
    self.lockdown_list=[]
    self.dead_people_list=[]
    self.dead_people=0
    self.death_steps=[]
  def population_initalize(self):
    IP = 0 #initial population
    LOP = [] #list of people
    while IP<self.NOP:
      person = Person(self.en,x=random.randint(0,SIZE_B-1),y=random.randint(0,SIZE_L-1))
      LOP.append(person)
      
      self.vacinated.append(person.immune)
      IP=IP+1
    self.working_list=LOP
    self.LOP=LOP
    return LOP
  
  def location_registry(self):
    posts = []
    for person in self.LOP:
      posts.append((person.x,person.y))
    #print(posts)
    return posts
  
  def step(self,psn,infected=None,contagion=False,no_movement=False):
    ipt = random.randint(1,4)
    if no_movement is True:
      ipt=5
    if ipt == 1:
       env,x,y,state=psn.move(1,infected,contagion)
    elif ipt == 2:
      env,x,y,state= psn.move(2,infected,contagion)
    elif ipt == 3:
      env,x,y,state=psn.move(3,infected,contagion)
    elif ipt == 4:
      env,x,y,state= psn.move(4,infected,contagion)
    elif ipt == 5:
      env,x,y,state= psn.move(5,infected,contagion)
    return env,x,y,state
 
  def population_movement(self,posts=None):   # ONe MOVEMENT
    self.contact_list.clear()
    for item in self.LOP:
      self.contact_list.append(False)
    if len(self.infected)==0:contagion=False
    else:contagion=True
   # print("check...","\n",self.en)    
    self.infected.clear()
    
    for person in self.lockdown_list:
        person.step_update(self.current_step)
        env,x0,y0,state0 = self.step(person,self.infected,contagion,no_movement=True)
        if person.Death()==True:
           self.lockdown_list.remove(person)
        
        if state0==True:self.infected.append((x0,y0))
        elif state0==False:
          if (x0,y0) in self.infected:self.infected.remove((x0,y0))    
        if person in self.LOP:
          self.contact_list[self.LOP.index(person)]=state0
          self.Total_Economy_perstep = self.Total_Economy_perstep + person.Earning()
        
   # print(self.contact_list)
 
    for person in self.working_list:
        person.step_update(self.current_step)
        env,x0,y0,state0 = self.step(person,self.infected,contagion,no_movement=False)
        if person.Death()==True:
          self.working_list.remove(person)
        
        if state0==True:self.infected.append((x0,y0))
        elif state0==False:
          if (x0,y0) in self.infected:self.infected.remove((x0,y0)) 
        if person in self.LOP:
          self.contact_list[self.LOP.index(person)]=state0   
          self.Total_Economy_perstep = self.Total_Economy_perstep + person.Earning()
        
 
  def vacination(self,LOP,x1,x2,y1,y2):
    for u in range(y1,y2):
      self.en[x1][u]=self.immune_code
      for p in range(x1,x2):
        self.en[p][u]=self.immune_code
 
    
    for person in self.LOP:
      if person.vacinated(x1,x2,y1,y2) == True and self.vacinated[self.LOP.index(person)]==False:self.vacinated[self.LOP.index(person)]=True
    return self.en
 
  def hospitalization(self,LOP,x1,x2,y1,y2):
    for u in range(y1,y2):
      self.en[x1][u]=self.hospital_code
      for p in range(x1,x2):
        self.en[p][u]=self.hospital_code
    for person in LOP:
      person.hospital(x1,x2,y1,y2)
 
  def initialize_infection(self):
      for r in range(0,1):
        rand = random.choice(self.LOP)
        rand.contact=True
 
  
  def economy_tracker(self):
    self.Total_income_list.append(self.Total_Economy_perstep)
  def display(self):
    print(self.en,"\n\n")
 
  def lockdown(self,percent=0):
    self.lockdown_percent = percent/100
    self.lockdown_list = random.sample(self.LOP,int(len(self.LOP)*self.lockdown_percent))
    self.working_list = []
    for sample in self.LOP:
      if sample not in self.lockdown_list:
        self.working_list.append(sample)
    print("+++++++++++++++++++++++++++++++++++ {} LOCKDOWN +++++++++++++++++++++++++++++++++++".format(percent))
 
  def non_display_stats(self,y,Limit):
    #print(len(self.LOP),len(self.lockdown_list),len(self.working_list))
    self.current_step = y+1
    self.current_step_lst.append(y)
    self.new_case = 0
    recovered_cases=0
    u=0
    
    if u==0:
      contact=0
      imune=[]
      immune=0
      
 
      for state in self.contact_list:
       if state==True:contact+=1
      if contact>self.prev_contacts:
        self.steps.append(y)
        self.cnt.append(contact)
        self.new_case =contact - self.prev_contacts
        self.new_case_list.append(self.new_case)
        self.new_case_steps.append(y)
 
      elif contact<self.prev_contacts:
        self.steps.append(y)
        self.cnt.append(contact)
        recovered_cases = self.prev_contacts-contact
        self.total_recovered_cases =  self.total_recovered_cases + (self.prev_contacts-contact)
        self.total_recovered.append(self.total_recovered_cases)
        self.recovery_list.append(recovered_cases)
        self.recovery_steps.append(y)
 
      self.prev_contacts=contact
 
      for immune_state in self.vacinated:
        if immune_state:immune+=1
 
      if immune>self.prev_immune:
        self.immune_steps.append(y)
        d=immune-self.prev_immune
        if d != 0:self.immune.append(immune)
      self.prev_immune=immune
      self.Total_Economy_perstep = 0
      
    if (self.dead_people - len(self.LOP))!=0:
      self.death_steps.append(y)
      self.dead_people_list.append(self.dead_people - len(self.LOP))
    self.dead_people=len(self.LOP)
 
    if contact==1 and len(self.recovery_list)!=0:
      for person in self.LOP:
        if person.contact==True:
          person.contact=False
   # print(self.contact_list)
    #print(self.dead_people_list,len(self.LOP))
    Total_deaths=0
    Total_death_list=[]
    for deaths in self.dead_people_list[1:]:
      Total_deaths=deaths+Total_deaths
      Total_death_list.append(Total_deaths)
    print("DAYS : ",y,"ToTal POpulation : ",len(self.LOP),"Active Cases : ",contact,"New Cases : ",self.new_case,"Recovery : ",recovered_cases,"IMMUNE : ",immune,"Deaths : ",Total_deaths)
    if y>Limit:
      #fig,ax = plt.subplots()
     # print(self.recovery_steps,self.total_recovered)
      print(self.cnt)
      plt.plot(self.steps,self.cnt,'red')
      #plt.plot(self.recovery_steps,self.total_recovered,'green')
      plt.plot(self.death_steps[1:],Total_death_list,color="Black")
      
      #plt.plot(self.immune_steps,self.immune,'blue')
      #plt.plot(self.new_case_steps,self.new_case_list,color="Red")
      #plt.plot(self.recovery_steps,self.recovery_list,color="green")
      #plt.set(xlabel='STeps', ylabel='PoPulation',
            #title='MonteCarloSimulation')
      plt.grid()
      plt.show()
 
 
      print(self.Total_income_list)
      TC=[]
      for income in self.Total_income_list:
        TC.append(income)
      plt.plot(self.current_step_lst,TC,color="green",linestyle="dashed")
      plt.grid()
      plt.show()
    return contact
 
 
 
SC = simulation_control(1000,en)
PI = SC.population_initalize()
print("POpulation INITIALIZING...")
day=0
Limit = 600
while True:
  day+=1
  
  #print(PI)
  #if day==250:SC.lockdown(60)
  if day ==2 :SC.initialize_infection()
  for t in range(0,30):
    SC.population_movement(SC.location_registry())
    if day>0:SC.hospitalization(PI,3,12,3,12)
    if day>7050:SC.vacination(PI,15,25,15,25)
  SC.economy_tracker()
  if day%1==0:SC.non_display_stats(day,Limit)
  #SC.display()
  time.sleep(0)
  if day>Limit:
    break

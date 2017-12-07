#!/usr/bin/python
import os
import unittest
import tempfile
import shutil

"""
This module is designed for managing enrolments for tutorial classes.
It was designed and developed By John Lakkis from RMIT University.
Use or distribution of this file is strictly prohibited and may not be 
reproduced under any circumstances without prior approval.
"""

def read_lines(filename):
    """Returns a list of all lines in the specified file in its original order
        except for line starting with a #. The lines returned do not end with a 
            new line character"""
             
    if os.path.exists(filename):
        #opening & reading in a file and setting variable 'list' to empty list
        filename = open(filename, "r")
        filename = filename.readlines()
        lists = []
        #removing any line that begins with a hash and also removing new lines
        #then adding all the content of the file into a list
        for lines in filename:
            if lines.startswith('#') == False:
                lines.lstrip('#')
                lines = lines.strip('\n')
                lists.append(lines)
        return lists
    else:
        #this function returns the string false if the file does not exist
        return 'False'


def read_table(filename):
    """Reads a file of colon delimited lines and returns a list of lists in the
        original order, with each line being represented as a list of strings, 
            split on colons. """
            
    if os.path.exists(filename):
        #opening & reading in a file and setting variable 'list' to empty list
        filename = open(filename, "r")
        filename = filename.readlines()
        lists = []
        #removing any line that begins with a hash and also removing new lines
        #then adding all the content of the file into a list
        for lines in filename:
            if lines.startswith('#') == False:
                lines.lstrip('#')
                lines = lines.strip('\n')
                lines = lines.split(':')
                lists.append(lines)
        return lists
    else:
        #this function returns the string false if the file does not exist
        return 'False'
    
    
def write_lines(filename, lines):
    """Writes a list of strings safely to the specified file. That is the file 
        is first saved as a temp file then once it is complete renames the 
            file to the specified file. If successful the function returns 1 
                otherwise a 0 is returned."""
    #creates a temporary file            
    tempFile = tempfile.NamedTemporaryFile(delete=False)
        
    try:
        for i in lines:
            tempFile.write(i + '\n')          
        #closes the temporary file
        tempFile.close()
        #renames the temp file to the filename specified 
        #os.rename(tempFile.name, filename)
        shutil.move(tempFile.name,filename)
        return 1
    except:
        return 0
  
   
class Enrol(object):
    """The class encapsulates the tutorial enrolment records. When an object of 
        the Enrol class is instantiated, it reads enrolment records from the 
        specified data directory. """
    def __init__(self,location):
        """It accepts an argument which is the path to the data directory where
            all the enrolment records are kept."""
        #store the working directory into the variable
        self.location = location
        
        try:    
            if os.path.exists(self.location):
                #reads in the files into the relative variables 
                self.subjectList = read_table(os.path.join(self.location,
                                                                'SUBJECTS'))
                self.classList = read_table(os.path.join(self.location,
                                                                    'CLASSES'))
                self.venue = read_table(os.path.join(self.location,
                                                             'VENUES'))
            #if the specified location does not exist raises a KeyError
            else:
                raise KeyError
        except KeyError:
            raise KeyError ('The specified directory does not exist')
     
            
    def subjects(self):
        """Returns a list of all subject codes in the enrolment system."""
        #sets courseCode to an empty list 
        courseCode = []
        #adds each subject code to a list and returns it 
        for lines in self.subjectList:
            lines = lines[0]
            courseCode.append(lines)
        return courseCode
    
        
    def subject_name(self, courseCode):    
        """Returns a string which is the name of the specified subject  """ 
        #sets dict1 to an empty dictionary 
        dict1 = {}
        #iterate through the subjectList file and sets a key and value pairs
        for (key, value) in self.subjectList:
            try:
                dict1[key].append( value )
            except:
                dict1[key] = value
        try: 
            courseCode in dict1.keys() 
            return dict1[courseCode]
        except KeyError: 
            raise KeyError('The course code '+courseCode+' does not exist!')
 
        
    def classes(self, courseCode):
        """Returns a list of class codes for the specified subject."""
        #creation of data structures(empty lists and empty dictionary) 
        newList = []
        classDictionary = {}
        newdict = {}
        #Iterates through classList and add specified contents to list
        for classList in self.classList:
            classList = classList[:2] 
            newList.append(classList)
        #Iteration assigns newList a key and value pair
        for (key, value) in newList:
            try:
                classDictionary[key].append( value )
            except:
                classDictionary[key] = value
        #Iterates over the value in the dictionary and swap the key and value
        for (key,value) in classDictionary.items():
            newdict.setdefault(value,[]).append(key)
       
        try: 
            courseCode in newdict.keys() 
            return newdict[courseCode]
        except KeyError: 
            raise KeyError ('The course code '+courseCode+' does not exist!')

               
    def class_info(self, class_Code):
        """Returns class information in a tuple, within the tuple return a list
            of enrolled student, if there ate no enrolled student returns an 
                empty list)."""
        #set new list to an empty list        
        newList = []
        testKeyError = 0  
        #reads in the specified roll file        
        classRoll = read_lines((os.path.join(self.location,
                                                    class_Code+'.roll'))) 
        #tests wheter the roll file exists if not sets classRoll to empty list
        if classRoll is 'False':
            classRoll = []
            hasRoll = 'False'
        else:
            hasRoll = 'True'
        #assigns all the values in the classList to newList  
        for (classes, classCode, time, room, teacher ) in self.classList:
            classInfo = (classes, classCode, time, room, teacher, classRoll)
            newList.append(classInfo)  
        #iterates over newList if there is no roll just returns the class info     
        for classes in newList:
            if class_Code in classes and hasRoll is 'False':
                testKeyError = 1
                return classes[1:]
            #if there is a roll file return class info
            elif class_Code in classes and hasRoll is 'True':
                testKeyError = 2
                return classes[1:]
        #if the course code does not exist raise a keyerror
        try:
            if testKeyError == 0:
                raise KeyError
        except KeyError:
            raise KeyError ('The course code ' +class_Code+ ' does not  exist') 
         
         
    def check_student(self, student_ID, subjectCode=None):
        """Return a list of all the classes a student is enrolled in if no 
            subject code supplied, if there is a subject code supplied only
                return the classes the student is enrolled for that subject.
                    If the student is not enrolled in any subjects will return
                        an empty list"""
        subjects = self.subjects()
        #set classRolls and cl to empty lists
        classRolls = []
        cl = []
        #if no subject code supplied return a list of all subjects and add
        #to classRolls list
        if subjectCode == None:
            for subjects in subjects:
                subject = self.classes(subjects)
                classRolls.extend(subject)
        #if subject code supplied but does not exist return None
        elif subjectCode not in subjects:
            return None
        #if subject code supplied and exists return the classes 
        else:
            classRolls = self.classes(subjectCode)
        #read in the roll file for the supplied classes     
        for classes in classRolls:
            classRoll = read_lines((os.path.join(self.location,
                                                    classes+'.roll')))
            #if the student is in the roll file add the classes to cl
            if student_ID in classRoll:
                cl.append(classes)
        #if the subjectCode is not supplied and cl is empty return cl  
        if subjectCode == None and cl == []:
            return cl
        if not cl:
            return None
        else:
            return cl
               
    def enrol(self, student_ID, class_Code):
        """Enrols student into class, returns 1 if successful ."""
        #stores the location of the roll file in classRoll_Location 
        classRoll_Location = os.path.join(self.location,class_Code+'.roll')
        #assigns value of class info indexes to variables  
        classInfo = self.class_info(class_Code)
        classRoom = classInfo[2]
        occupancy = len(classInfo[4])
        studentList = classInfo[4]
        subjectCode = classInfo[0]
        #assigns subject classes to allClasses
        allClasses = self.classes(subjectCode)
        #if the class code does not exist raise an error
        try:
            if class_Code not in allClasses:
                raise KeyError
        except KeyError:
            raise KeyError ('The class code ' + class_Code + ' does not exist')
        #check if the class is full 
        for classroom,capacity in self.venue:
            if classRoom == classroom:
                if  int(occupancy) >= int(capacity): 
                    return None   
             
        for eachClass in allClasses:
           
            checkALLclasses = self.class_info(eachClass)

            if len(allClasses) < 2:
                if student_ID in checkALLclasses[4]:
                    #this removes the student from the current enrolled class
                    studentList.remove(student_ID)
                    #this adds the student to the new class
                    studentList.insert(0, student_ID)
                    acknowledge = write_lines(classRoll_Location, studentList)
                    
                    return acknowledge
                elif student_ID not in checkALLclasses[4]:
                        #inserts the student into the new class
                    
                    studentList.insert(0, student_ID)
                      
                    acknowledge = write_lines(classRoll_Location,studentList)
                    
                    return acknowledge 
            else: 
                studentClasses = self.check_student(student_ID, 
                                                                subjectCode)
                if student_ID in checkALLclasses[4]:
                   
                    classInfo = self.class_info(*studentClasses)
                    classList = classInfo[4]
                    if class_Code in studentClasses:
                        #Removes the student from the current enrolled class
                        studentList.remove(student_ID)
                        #this adds the student to the new class
                        studentList.insert(0, student_ID)
                        acknowledge= write_lines(classRoll_Location, studentList)
                    
                        return acknowledge
                    elif class_Code not in studentClasses:
                        classList.remove(student_ID)
                        write_lines(os.path.join(self.location,
                                                 eachClass+'.roll'), classList)
                    #this adds the student to the new class
                        studentList.insert(0, student_ID)
                        acknowledge = write_lines(classRoll_Location, 
                                                                studentList)
                        return acknowledge
                    
                elif student_ID not in checkALLclasses[4]:
                    #inserts the student into the new class
                    studentList.insert(0, student_ID)
                    acknowledge = write_lines(classRoll_Location,studentList)
                    return acknowledge

class EnrolTest(unittest.TestCase):
    """This module tests the functions from enrol. It will return an error 
        where the results returned do not match the expected results"""
    
    def setUp(self):
        """Sets up a tempoary directory then write files to that directory that 
            will be used for testing scenarios"""   
        #set temporary directory     
        self.dir = tempfile.mkdtemp()
        #creates files and writes data to them 
        with open(os.path.join(self.dir,'CLASSES'), 'w+r') as self.classes:
            self.classes.writelines(
                ['scr101.1:scr101:Mon 9.30:2.5.10:Dr. Sullivan\n',
                    'scr102.1:scr102:Tue 14.30:2.6.1:Prof. Wazowski\n',
                        'scr102.2:scr102:Wed 14.30:2.6.1:Prof. Wazowski\n',
                            'scr202.A:scr202:Tue 15.30:23.5.32:Randy II\n' ])
            
            with open(os.path.join(self.dir,'SUBJECTS'), 'w+r') as self.subjects:
                self.subjects.writelines(['scr101:Intro to Scaring\n',
                    'scr102:History of Scaring\n', 
                        'scr202:Disappearing\n'])
                
                with open(os.path.join(self.dir,'VENUES'), 'w+r') as self.venues: 
                    self.venues.writelines(['2.5.10:3\n','Lab 2:8\n',
                                                '2.6.1:3\n','23.5.32:50\n'])
                    
                    with open(os.path.join(self.dir,'scr102.1.roll'),'w+r') as self.class1:
                        self.class1.writelines(['12345\n', '234567\n', '456789\n'])
                        
                        with open(os.path.join(self.dir,'scr102.2.roll'),'w+r') as self.class2:
                            self.class1.writelines(['54656\n', '85858\n', '95959\n'])
                            
                            with open(os.path.join(self.dir,'scr101.1.roll'),'w+r') as self.class3:
                                self.class1.writelines(['45698\n', '82258\n', '95759\n'])

    def test_readline(self):
        """Tests the read_lines function and checks the return value matches
                the expected returned value"""
        self.assertEqual(read_lines(self.venues.name), ['2.5.10:3', 'Lab 2:8', 
                                                '2.6.1:3', '23.5.32:50'])
        
    def test_readtable(self):
        """Tests the read_table function and checks the return value matches
                the expected returned value"""
                
        self.assertEqual(read_table(self.venues.name),[['2.5.10', '3'], 
                            ['Lab 2', '8'], ['2.6.1', '3'], ['23.5.32', '50']])
        
    def test_writelines(self):
        """Write data using the write_lines function and check the return value 
                matches the expected returned value"""
                
        self.assertEqual(write_lines(self.venues.name,['2.5.10:18\n',
                                'Lab 2:8\n','2.6.1:22\n','23.5.32:50\n']),1)

    def test_subjects(self):
        """Tests the subjects() function and checks the return value matches
                the expected returned value"""
        e = Enrol(self.dir)
  
        self.assertEqual(e.subjects(), ['scr101', 'scr102', 'scr202'])
        self.assertTrue(e.subjects(), ['scr101', 'scr102', 'scr202'])
        
    def test_subject_name(self):
        """Tests the subject_name() function and checks the return value 
                matches the expected returned value"""
        e = Enrol(self.dir)
        
        self.assertEqual(e.subject_name('scr101'), 'Intro to Scaring')
        
    def test_classes(self):
        """Tests the test_classes() function and checks the return value 
                matches the expected returned value"""
        e = Enrol(self.dir)
         
        self.assertRaises(KeyError, e.classes, 'scr101.')
        self.assertEqual(e.classes('scr101'), ['scr101.1'] )
        
    def test_class_info(self):
        """Tests class_info() function and checks the return value 
                matches the expected returned value"""
        e = Enrol(self.dir)
        
        self.assertRaises(KeyError, e.class_info, 'scr')
        self.assertEqual(e.class_info('scr202.A'), ('scr202', 'Tue 15.30', 
                        '23.5.32', 'Randy II', []) )
   
    def test_check_student(self):
        """Tests the check_student() function and checks the return value 
                matches the expected returned value"""
        e = Enrol(self.dir)
        
        self.assertEqual(e.check_student('s3018841'), []) 
        self.assertEqual(e.check_student('s3018841', 'scr102'), None)       
    
    def test_enrol(self):
        """Tests the enrol() function and checks the return value 
                matches the expected returned value"""
        e = Enrol(self.dir)
          
        self.assertEqual(e.enrol('85858', 'scr102.1'), None)
        self.assertEqual(e.enrol('45698', 'scr101.1'),1)
        self.assertRaises(KeyError, e.enrol, '45698', 'scr101.')
        
    def tearDown(self):
        """Removes the temporary directory once all the tests are complete"""
        shutil.rmtree(self.dir)
 
if __name__ == '__main__':
    unittest.main()
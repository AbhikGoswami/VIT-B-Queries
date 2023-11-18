import streamlit as st
from streamlit_chat import message

import sqlite3
import time

conn = sqlite3.connect('conversation.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        user_input TEXT,
        bot_response TEXT
    )
''')
conn.commit()

class QueryNode:
    def __init__(self, keywords, response):
        self.keywords = keywords
        self.response = response
        self.next = None

class QueryLinkedList:
    def __init__(self):
        self.head = None

    def add_query(self, keywords, response):
        new_node = QueryNode(keywords, response)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

class QueryCategoryTree:
    def __init__(self):
        self.categories = {}

    def add_category(self, category_name):
        if category_name not in self.categories:
            self.categories[category_name.lower()] = QueryLinkedList()

    def add_query_to_category(self, category_name, keywords, response):
        if category_name.lower() in self.categories:
            self.categories[category_name.lower()].add_query(keywords, response)

    def common_queries(self, category_name):
        if "common" in self.categories:
            common_list = self.categories["common"].head
            while common_list:
                self.add_query_to_category(category_name, common_list.keywords, common_list.response)
                common_list = common_list.next

    
    def get_response(self, category_name, user_input):
        
        if category_name in self.categories:
            current = self.categories[category_name.lower()].head
            user_input = user_input.lower()  
            
    
            while current:
                for keyword in current.keywords:
                    if keyword.lower() in user_input:
                        return current.response
                current = current.next
        
        return "I'm sorry, I don't have an answer for that."


query_bot= QueryCategoryTree()

query_bot.add_category("common")
query_bot.add_query_to_category("common",["leave proceedings","leave","outing"],"leave can be availed via proctor. One has to submit a leave request to the protor. The proctor on confirming with the student's parent can accept or reject a leave request. The further procedure will be done from the hostel supervisor's end.")
query_bot.add_query_to_category("common",["proctor-proctee","proctee","proctor"],"The proctor-proctee system is designed to provide support and guidance to students during their academic journey.\nA proctor is a faculty member who is assigned to a group of students, known as proctees. The proctor serves as a mentor, advisor, and guide to the proctees throughout their time at the university. The proctor is usually responsible for helping students with academic, personal, and career-related issues.")


query_bot.add_category("Hostels")
query_bot.common_queries("Hostels")
query_bot.add_query_to_category("Hostels", ["room","room type","variant","room categories"], "There are various room type and room categories available in both Boys and Girls hostel. such as:-\n1) 2 Bed AC/Non AC\n2) 3 bed AC/Non AC\n3) 4 bed AC/Non AC\n4) 5 bed AC/Non AC\n5) 6 bed AC/Non AC.\nThe availability and allocation of rooms is purely based on the Hostel councelling process.\n\nFor more detailed information about the fees structure, kindly visit https://vitbhopal.ac.in/hostel-life/")
query_bot.add_query_to_category("Hostels", ["hostel rules", "accommodation policies"], "Hostel rules can be found on the university website.")
query_bot.add_query_to_category("Hostels", ["mess timings","food timings","food timing","meal","breakfast","lunch","dinner","snacks"], "\nBreakfast 7:30-9:00\nLunch 12:30-2:00\nSnacks 5:00-6:00\nDinner 7:30-9:00\n")
query_bot.add_query_to_category("Hostels",[("caterers" or "mess" or "mess service" or "catering") and "girls hostel"],"For Girls hostel Block 1 we have AB-Mess and for Block 2 we have Mayuri caterers")
query_bot.add_query_to_category("Hostels",[("caterers" or "mess" or "mess service" or "catering") and "boys hostel"],"For Boys hostel Block 1 we have CRCL-mess and for Block 2-5 we have Mayuri caterers.")
query_bot.add_query_to_category("Hostels",["caterers", "food service","catering"],"For Girls hostel Block 1 we have AB-Mess and for Block 2 we have Mayuri caterers\n     For Boys hostel Block 1 we have CRCL-mess and for Block 2-5 we have Mayuri caterers.")
query_bot.add_query_to_category("Hostels",["ammenities","Necessary ammeneties","amenities","facilities"],"There is 24x7 internet service in the hostel premises.\n     There is health centre and ambulance for the medical attentions of the hostellers.\n     There is parlour and Salon for both boys and girls.\n     Indoor game facilities and night canteen is also there for recreation purposes of the students.")
query_bot.add_query_to_category("Hostels",["councelling","Hostel concelling","counselling"],"You have to fill your room choices (say two bedded AC room, three bedded non AC room). In first semester based on VITEEE rank you will be allotted in a room in a particular block. From next semester onwards , room will be allocated based on hostel index rank (based on CGPA and attendance).")


query_bot.add_category("Academics")
query_bot.common_queries("Academics")
query_bot.add_query_to_category("Academics", ["Change of programme","migartion","migarte","branch","branch change"], "The change in program/branch is possible after 1st year after maintaining a certain level of CGPA with the permission of the respective program chair. For more details contact with the Program Chair.")
query_bot.add_query_to_category("Academics", ["academic calender", "semester schedule"], "The academic calendar is available on VTOP(https://vtop.vitbhopal.ac.in/vtop/initialProcess)")
query_bot.add_query_to_category("Academics", ["faculty","faculty type","faculties"], "There is 100% Doctoral faculty at VIT Bhopal. Please visit https://vitbhopal.ac.in/faculty/ for more details about faculties.")
query_bot.add_query_to_category("Academics", ["Exam regulations","exam rules","regulations"], "All the examinations in the university is conducted and regulated by the COE office. For more details refer to:- https://vitbhopal.ac.in/controller-of-examinations/")
query_bot.add_query_to_category("Academics",["pedagogy","teaching pedagody","method","method of teaching","Caltech","cal","cal-tech"],"Here at VIT Bhopal we follow Collaborating and Active Learning through technology(CALTECH) method of learning.\nCALTech – Collaborative and Active Learning through Technology is a unique, first-of-its-kind academic and research initiative, exclusively crafted by VIT Bhopal University. It aims at providing a holistic, interactive environment for an intensely gratifying learning experience, for the students. The classrooms have ‘No Blackboard & No Back Benches’. Learning here is through “Collaborative & Active Learning through Technology (CALTech)”, where the laboratories and classrooms have been integrated as studios offering technology enabled learning. While learning in this manner students tend to perform at a much higher level, exhibiting skills which could not be accomplished in a conservative passive teaching methodology.")
query_bot.add_query_to_category("Academics",["FFCS","timetable"],"Student can make their own timetable through FFCS(Fully Flexible Credit System).\nThis allows more flexibility to a student as per their priorities")
query_bot.add_query_to_category("Academics",["attendance"],"There is a minimum attendance criteria of 75%. Below that a student can be debarred from giving examinations.")
query_bot.add_query_to_category("Academics",["grading policy of exams","grade policy","marking policy","basis of grading","grade","marking"],"Both Midterm and TermEnd are scaled to 30 then 40 marks from internals is added. Then grades are given based on class performance in each subject. Based on these grades, final GPA of each semester is calculated. Lastly CGPA is calculated from all GPAs of all semesters. Internal marks are given on the basis of practicals, tutorials, quizzes, assignments and attendance(carries 0-5 marks based on your attendance percentange).")
query_bot.add_query_to_category("Academics",["semester exams","many exams","exams in semester","exams","types of exams","examinations","types of examinations"],"There are two exams per semester. midterm of 50 marks and Term End of 100 marks.\n     Failure of passing any semester leads to arrear or supplementary exams.")
query_bot.add_query_to_category("Academics",["pass","passing criteria","pass criteria","passing policy","exam pass"],"For Midterm, it is 20 and for TermEnd it is 40. You have to score 60 overall in Midterm + TermEnd to pass a subject.")
query_bot.add_query_to_category("Academics",["contact faculty" or "contact program chair" or "contact dean" or "contact" or "contact details"],"A)	In VTOP under Faculty Info of Academics section, you can search for any faculty. It will provide you their email address and cabin number.")
query_bot.add_query_to_category("Academics",["credit required","Number of credits","credits","credit","credit system"],"Programme Core 55\nProgramme Elective 15\nOpen Elective 21\nNatural Science, Humanities and Management 69\nTotal 160 credits are needed.")


query_bot.add_category("Admission Process")
query_bot.common_queries("Admission Process")
query_bot.add_query_to_category("Admission Process",["entrance exam","exam","admission process","admission"],"For UG BTech. admissions there is a centralised exam VITEEE for all the four campuses of VIT.\n     The selection is purely based on the counselling as per merit rankings.")                                                       

query_bot.add_category("General Information")
query_bot.add_query_to_category("General Information",["location","located","situated"],"VIT Bhopal university is located in Kotri Kalan, Ashta, Near, Indore Road, Bhopal, Madhya Pradesh 466114.\n     Refer to the google map location:- https://maps.app.goo.gl/6oFTztrqFYbYnhMs8")
query_bot.add_query_to_category("General Information",["how to reach","how to get there","route","ways of reaching","reach","come"],"From Bhopal Railway Station Use public transport/cab to reach Lalghati Square (approx. 9 kms). VIT Bhopal campus is approx. 62 kms from Lalghati Square, on Bhopal-Indore highway, 3 kms away from the 2nd Tollplaza. Intercity Volvo A/C buses are available through the day.\n     From Bhopal Airport Use public transport/cab to reach Lalghati Square (approx. 9 kms). VIT Bhopal campus is approx. 62 kms from Lalghati Square, on Bhopal-Indore highway, 3 kms away from the 2nd Tollplaza. Intercity Volvo A/C buses are available through the day.\n     From Indore Airport Use public transport/cab to reach Star square (approx. 15km). VIT Bhopal campus is approx. 120 kms from Star Square, on Indore-Bhopal highway. Intercity Volvo A/C buses are available through the day.")

query_bot.add_category("Campus Life")
query_bot.add_query_to_category("Campus Life",["clubs","ECA","Extra curriculur activities"],"There are more than 50 technical, non technical and regional clubs here at VIT Bhopal. Students can register for them under Extra Curriculur Activities.")
query_bot.add_query_to_category("Campus Life",["Events","fests"],"There are number of technical and cultural events taking place every now and then in the university. This ensures recreation and enjoyments of students apart from studies.\n     Also there is an annual Techno-Cultural fest ADVITYA, which is held every year.")
query_bot.add_query_to_category("Campus Life",["Religious Celebrations","celebrations","festivals"],"Different Religious ceremonies are held in the university which are conducted by the respective regional club in the university. For example:- Ganesh Chaturthi, Onam. etc")

st.set_page_config(
    page_title="VIT-B Queries", 
    page_icon="https://plus.unsplash.com/premium_photo-1677252438450-b779a923b0f6?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    layout="wide", 
    initial_sidebar_state="auto")

st.title("VITB Queries")

changes = '''
<style>
[data-testid="stAppViewContainer"]
{
background-image:url('https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
background-size:100%,100%;
}

html{
background:transparent
}

div.ea3mdgi6 > iframe
{
background-color:transparent
}

</style>
'''

st.markdown(changes, unsafe_allow_html=True)

category_name = st.selectbox("Select a category:", ["Hostels","Academics","Admission process","General Information","Campus Life"]).lower()

print(st.session_state)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


user_input = st.text_input("YOU: ", key="b").lower()

if st.button("Ask"):
    response = query_bot.get_response(category_name, user_input).lower()
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], key="user_" + str(i), is_user=True)
        message(st.session_state['generated'][i], key=str(i))

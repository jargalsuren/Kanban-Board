import unittest
from kanban import kanban, Task, User

class Test_kanban(unittest.TestCase):
    
    def test_signup_page(self):
        '''
        Testing if the sign up page is loaded OK.
        '''
        req = self.app.get('/', follow_redirects=True)
        self.assertEqual(req.status_code, 200)
    
    def test_login_page(self):
        '''
        Testing if the login page is loaded OK.
        '''
        req = self.app.get('/login', follow_redirects=True)
        self.assertEqual(req.status_code, 200)
    
    def test_dashboard_page(self):
        '''
        Testing if the Kanban Board dashboard page is loaded OK.
        '''
        req = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(req.status_code, 200)
    
    def test_addtask_page(self):
        '''
        Testing if the adding task page is loaded OK.
        '''
        req = self.app.get('/add_task', follow_redirects=True)
        self.assertEqual(req.status_code, 200)
    
    def test_create(self):
        '''
        Testing the task creation.
        '''
        testing = 'Testing'
        #Create a new task
        req = self.kanban.post(
            '/add_task', data=dict(title=testing), follow_redirects=True)
        #remove the tasks added
        act = Task.query.filter_by(title=testing).first()
        self.kanban.get('/delete/'+str(act.id), follow_redirects=True)
        #Checking request status code
        self.assertEqual(req.status_code, 200)
        
    def test_update(self):
        '''
        Testing the status update.
        '''
        testing = 'Update'
        #Adding task
        self.kanban.post('/add_task',
                      data=dict(title=testing),
                      follow_redirects=True)
        #Query the task
        act = Task.query.filter_by(title=testing).first()
        #Get the status update
        req = self.kanban.get('/update/'+str(act.id) +
                           '/Doing', data=dict(id=act.id))
        #remove the tasks added.
        act2 = Task.query.filter_by(title=testing).first()
        #check whether the response status for update method is correct.
        self.kanban.get('/delete/'+str(act2.id), follow_redirects=True)
        self.assertEqual(req.status_code, 302)
    
    def test_delete(self):
        '''
        Testing the task deletion
        '''
        testing = 'Delete'
        self.app.post('/add_task',
                      data=dict(title=test_title),
                      follow_redirects=True)
        #Querying the task
        act = Task.query.filter_by(title=test_title).first()
        #Delete the task
        req = self.app.get('/delete/'+str(act.id), follow_redirects=True)
        #checking the status code
        self.assertEqual(req.status_code, 200)


if __name__ == "__main__":
    unittest.main()

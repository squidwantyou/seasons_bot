import sys,os

class Mfc:
    def __init__(self, t = 2):
        if t == 2:
            self.type = "2"
            self.status = "Recruiting"
            self.recruit_left = 2
            self.account = list()
            self.flowtype = "1by1"
            self.gid = None

    def conduct(self,m,uid,gid):
        print(self.status)
        sys.stdout.flush()

        if self.status == "Recruiting":
            assert self.recruit_left > 0
            if not self.gid :
                self.gid = gid
                self.account.append(uid)
                self.recruit_left -= 1
            else:
                if uid not in self.account:
                    self.account.append(uid)
                    self.recruit_left -= 1
                else:
                    return "Ignore"

            if self.recruit_left == 0:
                print("DEBUG END recruit")
                sys.stdout.flush()
                self.status = "End_Recruit"
                if self.flowtype == '1by1':
                    self.waiting = list()
                    self.waiting.append( self.account[0] )
                    self.status = f'Wait {",".join( [str(x) for x in self.waiting] )}'
            return self.status

        if "Wait" in self.status:
            print(">>>> DEBUG wait list:",self.waiting, uid )
            sys.stdout.flush()
            if self.flowtype == "1by1":
                if uid in self.waiting and gid == self.gid:
                    c_index = self.account.index(uid)
                    next_index = c_index + 1
                    next_index = next_index % len(self.account )
                    self.waiting = list()
                    self.waiting.append( self.account[next_index] )
                    self.status = f'Wait {",".join( [str(x) for x in self.waiting] )}'
                    return self.status
                else:
                    return "Ignore"
            
            

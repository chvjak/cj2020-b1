import sys
f = sys.stdin
ferr = sys.stderr

DEBUG = False
#DEBUG = True


class MyJudge:
    def __init__(self, R, X, Y):
        self.X = X
        self.Y = Y
        self.R = R

    def read(self, query):
        X, Y = [int(x) for x in query.split(" ")]
        if self.X == X and self.Y == Y:
            self.response = "CENTER"
        else:
            if (self.X - X)**2 + (self.Y - Y)**2 <= self.R**2:
                self.response = "HIT"
            else:
                self.response = "MISS"


    def send(self):
        return self.response

#JUDGE = MyJudge(R=10**9 - 50, X=11, Y=12)
#JUDGE = MyJudge((10 ** 9) - 5, X=0, Y=0)
JUDGE = MyJudge((10 ** 9) - 5, X=5, Y=-5)

#JUDGE = MyJudge((10 ** 9) - 50, X=-50, Y=50)
#JUDGE = MyJudge((10 ** 9) - 50, X=0, Y=0)

#JUDGE = MyJudge(100, X=-999999900, Y=-999999900)
#JUDGE = MyJudge(5*10**8, X=-5*10**8, Y=-5*10**8)


def Log(msg):
    if DEBUG:
        print(msg, file=ferr)
        ferr.flush()

class JudgeClient:
    def __init__(self):
        self.i = 0

    def send(self, x, y):
        self.i += 1
        msg = "{0} {1}".format(int(x), int(y))
        Log("{0}) Sending: {1}".format(self.i, msg))

        if DEBUG:
            JUDGE.read(msg)
        else:
            print(msg)
            sys.stdout.flush()
    
        Log("Done sending")

    def read(self):
        Log("Reading response")

        if DEBUG:
            msg = JUDGE.send()
        else:
            msg = f.readline().strip()

        Log("Read response {0}".format(msg))

        return msg 

class FunctionX:
    def __init__(self, jc):
        self.jc = jc
        self.y = 0

    def __call__(self, x):
        self.jc.send(x, self.y)
        response = self.jc.read()

        if response == "CENTER":
            raise UnexpectedCenterFound()

        return 1 if response == "HIT" else -1 if response == "MISS" else 0

class FunctionY:
    def __init__(self, jc):
        self.jc = jc
        self.x = 0

    def __call__(self, y):
        self.jc.send(self.x, y)
        response = self.jc.read()

        if response == "CENTER":
            raise UnexpectedCenterFound()

        return 1 if response == "HIT" else -1 if response == "MISS" else 0

def bsect(a, b, f):
    if f(a) * f(b) < 0:
        while abs(a - b) > 1:
            c = (a + b) // 2
            if f(a) * f(c) < 0:
                a, b = a, c
            else:
                a, b = c, b
    else:
        assert False , "Shouldn't happen"

    return a

class UnexpectedCenterFound(Exception):
    pass

if not DEBUG:
    Log("Reading input")
    T, MinR, MaxR = [int(x) for x in f.readline().split(" ")]
    Log("Read {0}, {1}, {2}".format(T, MinR, MaxR))
else:
    T = 2
    MinR = JUDGE.R

MAX = 10 ** 9
jc = JudgeClient()
fx = FunctionX(jc)
fy = FunctionY(jc)

for t in range(T):
    try:
        jc.i = 0

        # find a point inside the dart board
        circle_fit_times = int(2 * MAX / MinR); #2 Max / 2R
        for r in range(circle_fit_times):
            for c in range(circle_fit_times):
                x0, y0 = -MAX + r * MinR, -MAX + c * MinR
                jc.send(x0, y0)
                response = jc.read()
                if response == "HIT":
                    break
                else:
                   if response == "CENTER":
                    raise UnexpectedCenterFound()
            if response == "HIT":
                break
        else:
            # should not happen
            jc.send(MAX * 4, MAX * 4)
            #sys.exit(1)

        # we fix y==y0
        fx.y = y0

        # while we are not out of circle, do bs looking for X of intersection
        a = -MAX
        b = x0  
        A = bsect(a, b, fx) if fx(a) == -1 else a

        # Find second intersection of chord
        a = x0
        b = MAX 
        B = bsect(a, b, fx)  if fx(b) == -1 else b

        # Find perpendicular to chord intersections
        # we fix x equal to center of chord
        fy.x = (A + B) // 2

        a = y0
        b = MAX 
        C = bsect(a, b, fy) if fy(b) == -1 else b

        MB = abs(A - B) // 2
        MC = abs(C - y0)

        if MC == 0:
            a = y0
            b = -MAX 
            D = bsect(a, b, fy) if fy(b) == -1 else b

            MD = abs(D - y0)
        else:
            MD = MB * MB / MC

        xc = A + MB
        yc = C - (MD + MC) // 2

        jc.send(xc, yc)
        response = jc.read()
        if response != "CENTER":
            # start growing the square around xc, yc
            S = 3
            while True:
                T = yc + S // 2
                B = yc - S // 2
                L = xc - S // 2
                R = xc + S // 2

                points = []

                # bootom of square
                points += [(L + i, B) for i in range(S)]

                # top of square
                points += [(L + i, T)  for i in range(S)]

                # left edge
                points += [(L, B + i)  for i in range(S)]

                # right edge
                points += [(R, B + i)  for i in range(S)]
                    
                for x1, y1 in points:
                    jc.send(x1, y1)
                    response = jc.read()
                    if response == "CENTER":
                        break

                if response == "CENTER":
                    break
                else:
                    S += 2

    except UnexpectedCenterFound:
        Log("UnexpectedCenterFound")

   
# Biggest delays
# 1) error in bsect - missing abs()
# 2) interactive debugger 
#   doesn't report error if wrong path
#   python path was not set after reinstall :(
#   python started from vs has weird arguments and doesn't run as expected BUT not on the laptop
# 3) border cases
#       circle can overlap the border
#       accidental hit of center / border
# 4) HUGE: RE on last test case
#       incorrecly calculated the grid / did not visualised/envisioned

#python C:\Users\Dmytro\source\repos\cj2020-b1\cj2020-b1\interactive_runner.py python C:\Users\Dmytro\source\repos\cj2020-b1\cj2020-b1\testing_tool.py 2 -- python C:\Users\Dmytro\source\repos\cj2020-b1\cj2020-b1\darts.py
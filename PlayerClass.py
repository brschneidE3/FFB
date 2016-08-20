__author__ = 'brendan'


class Player:

    def __init__(self,
                 name,
                 team,
                 pos,
                 list_of_points):

        self.name = name
        self.team = team
        self.pos = pos
        self.points = {}
        self.bye_week = None
        for i in range(len(list_of_points)):
            week = i+1
            points = list_of_points[i]
            if points == '-':
                self.bye_week = week
                points = 0.
            else:
                points = float(points)
            self.points[week] = points
        self.total = int(sum(self.points.values()))

    def __repr__(self):
        return "%s - %s" % (self.name, self.team)

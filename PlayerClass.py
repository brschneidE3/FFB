__author__ = 'brendan'


class Player:

    def __init__(self,
                 name,
                 team,
                 pos,
                 list_of_points,
                 avg_pick):

        self.name = name
        self.team = team
        self.position = pos
        self.points = {}
        self.bye_week = None
        self.avg_pick = float(avg_pick)
        for i in range(len(list_of_points)):
            week = i+1
            points = list_of_points[i]
            if points == '':
                self.bye_week = week
                points = 0.
            else:
                points = float(points)
            self.points[week] = points
        self.total = int(sum(self.points.values()))

    def __repr__(self):
        return "%s/%s" % (self.name[:15], self.team)

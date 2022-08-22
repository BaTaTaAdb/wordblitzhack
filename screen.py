class Screen:
    def __init__(self, resolution, pos1, pos2):
        self.resoltion = resolution
        # pos1(x,y)
        self.posmaxxy = (
            pos1[0] if pos1[0] > pos2[0] else pos2[0],
            pos1[1] if pos1[1] > pos2[1] else pos2[1]
        )
        self.posminxy = (
            pos1[0] if pos1[0] < pos2[0] else pos2[0],
            pos1[1] if pos1[1] < pos2[1] else pos2[1]
        )
        print(f"Point MIN: {str(self.posminxy)}")
        print(f"Point MAX: {str(self.posmaxxy)}")

    def get_top_box(self):
        return self.posminxy[1]

    def get_left_box(self):
        return self.posminxy[0]

    def get_width(self):
        return self.posmaxxy[0] - self.posminxy[0]

    def get_height(self):
        return self.posmaxxy[1] - self.posminxy[1]

    def get_mon(self):
        top = self.get_top_box()
        left = self.get_left_box()
        width = self.get_width()
        height = self.get_height()
        return {"top": top, "left": left, "width": width, "height": height}
class matrix(object):

    def __init__(self, data, width = -1, height = -1):

        self.data = []

        self.width = width

        self.height = height

        if type(data) != list:

            return

        if False not in list(map(lambda x: type(x) == list, data)) and len(data) > 0: # If all items in the list are lists

            self.height = len(data)

            self.width = len(data[0])
            
            data = [data[i][o] for i in range(self.height) for o in range(self.width)]

        elif width < 0 or height < 0:

            self.width = len(data)

            self.height = 1
            
        for i in range(self.height):

            self.data.append([])

            for o in range(self.width):

                self[i].append(0)

                if len(data) >= self.width * self.height:

                    self[i][o] = data[o + (i * self.width)]

    def __str__(self):

        output = "["

        for i in range(self.height):

            output += "\n\t["

            for o in range(self.width):

                output += "{}{}".format(str(self[i][o]), ", " if o + 1 < self.width else "")

            output += "]"
        
        output += "\n]"

        return output
    
    def __getitem__(self, key):

        return self.data[key]
    
    def __add__(self, other):

        return self.combine_matrix(other)
    
    def __iadd__(self, other):

        self.data = (self + other).data

        return self
    
    def __sub__(self, other):

        return self.combine_matrix(other, sub=True)
    
    def __isub__(self, other):

        self.data = (self - other).data

        return self
    
    def __mul__(self, other):

        return self.dot(other)

    def __imul__(self, other):

        self.data = (self.dot(other)).data

        return self

    def __rmul__(self, other):
        
        if type(other) == matrix:

            return other.dot(self)
        
        else:

            return self * other

    def combine_matrix(self, other, sub=False):

        if type(other) == matrix:

            if self.width == other.width and self.height == other.height:

                # Comprehensively construct list of added values (if sub is true, the second value becomes negative to subtract)
                data = [self[i][o] + (other[i][o] if not sub else -other[i][o]) for i in range(self.height) for o in range(self.width)]

                return matrix(data, width=self.width, height=self.height)

            else:

                raise TypeError("Cannot add matrices of different dimensions")

        else:

            raise TypeError("Cannot add type matrix with non-matrix type")

    def dot(self, other):

        if type(other) == matrix:
                
            result = matrix([], other.width, self.height)

            if self.width == other.height:

                for row_index in range(self.height):

                    for other_column_index in range(other.width):

                        column_sum = 0

                        for column_index in range(self.width):

                            column_sum += self[row_index][column_index] * other[column_index][other_column_index]

                        result[row_index][other_column_index] = column_sum

                return result
        
        elif type(other) == int or type(other) == float:
                
            result = matrix([], self.width, self.height)

            for row_index in range(self.height):

                for column_index in range(self.width):

                    result[row_index][column_index] = self[row_index][column_index] * other
            
            return result

        raise TypeError("Cannot multiply matrices where left width is not equal to right height")
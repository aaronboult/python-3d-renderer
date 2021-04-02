class matrix_base(object):

    def __init__(self, data, width, height):

        self.data = data

        self.width = width

        self.height = height

    def __str__(self):

        output = "["

        for i in range(self.height):

            output += "\n\t["

            for o in range(self.width):

                output += "{}{}".format(str(self.data[i][o]), ", " if o + 1 < self.width else "")

            output += "]"
        
        output += "\n]"

        return output
    
    def __getitem__(self, key):

        return self.data[key]

    def combine(self, other, sub=False):

        if isinstance(other, matrix_base):

            if self.width == other.width and self.height == other.height:

                # Comprehensively construct list of added values (if sub is true, the second value becomes negative to subtract)
                data = [
                    self.data[i][o] + (
                        other.data[i][o] if not sub else -other.data[i][o]
                    ) for i in range(self.height) for o in range(self.width)
                ]

                if self.width == 1:

                    return vector(data, self.height)

                else:

                    return matrix(data, width=self.width, height=self.height)

            else:

                raise TypeError("Cannot add matrices or vectors of different dimensions")

        else:

            raise TypeError("Cannot add type matrix with non-matrix base type")

class matrix(matrix_base):

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
    
    def __add__(self, other):
        
        return super().combine(other)
    
    def __iadd__(self, other):

        self.data = (super().combine(other)).data

        return self
    
    def __sub__(self, other):

        return super().combine(other, True)
    
    def __isub__(self, other):

        self.data = (super().combine(other, True)).data

        return self
    
    def __mul__(self, other):

        return self.dot(other)

    def __imul__(self, other):

        result = self.dot(other)
        
        self.data = result.data
        self.width = result.width
        self.height = result.height

        return self

    def __rmul__(self, other):
        
        if isinstance(other, matrix):

            return other.dot(self)
        
        return self.dot(other)

    def dot(self, other):

        if isinstance(other, matrix_base):
                
            result = matrix([], other.width, self.height)

            if self.width == other.height:

                for row_index in range(self.height):

                    for other_column_index in range(other.width):

                        column_sum = 0

                        for column_index in range(self.width):

                            column_sum += self[row_index][column_index] * other.data[column_index][other_column_index]

                        result[row_index][other_column_index] = column_sum

                return result
        
        elif type(other) == int or type(other) == float:
                
            result = matrix([], self.width, self.height)

            for row_index in range(self.height):

                for column_index in range(self.width):

                    result[row_index][column_index] = self[row_index][column_index] * other
            
            return result

        raise TypeError("Cannot multiply matrices where left width is not equal to right height")

class vector(matrix_base):

    def __init__(self, data = [], height = -1):
        
        if height == -1:

            height = len(data)
        
        if len(data) != height:

            data = [0 for i in range(height)]
        
        data = [[i] for i in data]

        super().__init__(data, 1, height)
    
    @property
    def x(self):
        if self.height > 0:
            return self[0]
        return None
    
    @x.setter
    def x(self, value):
        self[0] = value
    
    @x.deleter
    def x(self, value):
        del self[0]
    
    @property
    def y(self):
        if self.height > 1:
            return self[1]
        return None
    
    @y.setter
    def y(self, value):
        self[1] = value
    
    @y.deleter
    def y(self, value):
        del self[1]
    
    @property
    def z(self):
        if self.height > 2:
            return self[2]
        return None
    
    @z.setter
    def z(self, value):
        self[2] = value
    
    @z.deleter
    def z(self, value):
        del self[2]
    
    def __str__(self):
        
        return super().__str__()
    
    def __getitem__(self, key):

        return super().__getitem__(key)[0]

    def __setitem__(self, key, value):
        
        self.data[key][0] = value
    
    def __add__(self, other):

        return super().combine(other)
    
    def __iadd__(self, other):

        self.data = (super().combine(other)).data

        return self
    
    def __sub__(self, other):

        return super().combine(other, True)
    
    def __isub__(self, other):

        self.data = (super().combine(other, True)).data

        return self
    
    def __mul__(self, other):

        if isinstance(other, matrix):

            return other.dot(self)
        
        return self.multiply(other)
    
    def __rmul__(self, other):

        return self * other
    
    def __imul__(self, other):

        if isinstance(other, matrix):

            result = other.dot(self)

        else:

            result = self.multiply(other)
        
        self.data = result.data
        self.width = result.width
        self.height = result.height

        return self
    
    def multiply(self, other):
                
        result = vector([], self.height)

        if isinstance(other, vector):

            if self.height == other.height:

                for row_index in range(self.height):

                    result[row_index] = self[row_index] * other[row_index]

                return result
            
            else:

                raise TypeError("Vectors must be of same height to be multiplied")
        
        elif type(other) == int or type(other) == float:

            for row_index in range(self.height):
                
                result[row_index] = self[row_index] * other
            
            return result
        
        raise TypeError("Cannot multiply vector by non-vector or non-scalar types")
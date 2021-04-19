#Filip Wagner 92387
#source-->https://stackoverflow.com/questions/55437217/pseudo-code-algorithm-for-knapsack-problem-with-two-constrains?fbclid=IwAR0MsDxHx5Q6-HRv-BMMqdhYdy-AhGJ0BAeGGL0waDOGJ6y42BizfiJd5ko

#item class na lepsi pristup k vlastnostiam predmetov
class item:

    def __init__(self,id,value,weight,fragility):
        self._id=id
        self._value=value
        self._weight=weight
        self._fragility=fragility
    def setweight(self,weight):
        self._weight=weight
    def setvalue(self,value):
        self._value=value
    def setid(self,id):
        self._id=id
    def setfragility(self,frag):
        self._fragility=frag
    def getweight(self):
        return self._weight

    def getvalue(self):
        return self._value
    
    def getfragility(self):
        return self._fragility
    def getid(self):
        return self._id
    
    def __str__(self):
        return f"Id of item is: {self._id}, Value is: {self._value}, Weight is: {self._weight}, Fragility is: {self._fragility}"
        
#classa na vytvorenie knapsacku, kde vytvarame 3D matrix a pole itemov na vyber
class Knapsack:
    def __init__(self,maxweight,maxitems,maxfragility):
        self._maxweight = int(maxweight)
        self._maxitems = int(maxitems)
        self._maxfragility = int(maxfragility)


#source--> https://stackoverflow.com/questions/13445402/knapsack-algorithm-with-2-properties-how-to-implement-that-in-a-3d-array
#source-->https://www.youtube.com/watch?v=8LusJS5-AGo&list=PLpeMwo-2zP8iPCJikiiLvIKqzj8qX-oR8&index=39&t=729s
    def make_matrix(self,list_of_items):
        Matrix=[[[0 for z in range((int(self._maxfragility)+1))] for y in range((self._maxweight)+1)]for x in range((self._maxitems)+1)]

        for i in range(self._maxitems+1):
             for j in range(self._maxweight+1):
                  for k in range(self._maxfragility+1):
                      if (list_of_items[i].getweight() > j or list_of_items[i].getfragility() > k):
                          Matrix[i][j][k] = Matrix[i - 1][j][k]

                      elif list_of_items[i].getfragility() > k:
                          Matrix[i][j][k]=Matrix[i-1][j][k]

                      else:
                        Matrix[i][j][k]=max(Matrix[i-1][j][k],Matrix[i-1][j-list_of_items[i].getweight()][k-list_of_items[i].getfragility()]+list_of_items[i].getvalue())

        return Matrix
#source--> https://www.geeksforgeeks.org/printing-items-01-knapsack/
    def choose_items(self,matrix,list_of_items):
        chosen_items=[]
        for i in range(self._maxitems,0,-1):

            if (matrix[i][self._maxweight][self._maxfragility] > matrix[i-1][self._maxweight][self._maxfragility]):

                chosen_items.append(list_of_items[i])
                if list_of_items[i].getfragility()==1:
                    self._maxfragility-=1
                self._maxweight-=list_of_items[i].getweight()

        return chosen_items




class itemloader:
    def __init__(self,file_name):
        self._file=file_name
        self.maximumAllowedItems = 0
        self.maximumAllowedWeight = 0
        self.maximumAllowedFragileItems = 0

    def load_data(self):
        list_of_items=[]
        list_of_items.append(item(0,0,0,0))
        with open(self._file) as textFile:
            lines = [line.split(",") for line in textFile]
            big_list=[]
            for i in lines:
                for j in i:
                    j=j.replace("\n","")
                big_list.append(j.split(" "))
        self.maximumAllowedItems=big_list[0][0]
        self.maximumAllowedWeight=big_list[1][0]
        self.maximumAllowedFragileItems=big_list[2][0]

        for i,items in enumerate(big_list,0):
            if i>2:
                new_obj=item(int(items[0]),int(items[1]),int(items[2]),int(items[3]))
                list_of_items.append(new_obj)

        return self.maximumAllowedItems,self.maximumAllowedWeight,self.maximumAllowedFragileItems,list_of_items

class datasaver:
    def __init__(self,list_of_chosen):
        self._list_items=list_of_chosen

    def save_items(self):
        sum=0
        item_count=0
        with open("backpack_output.txt","w") as file:
            for item in self._list_items:
                file.write('%s\n' %item)
                sum+=item.getvalue()
                item_count+=1
            file.write('optimalna hodnota ruksaku je: %s\n' %sum)
            file.write('pocet itemov v riksaku je: %s\n' % item_count)

            file.close()
        print('Vystup je v subore backpack_output.txt')

class PackedKnapsack:
    def __init__(self):
        self.my_packed_bag="Not packed"
        self.final_sum=0


    def pack_my_bag(self,items):
        max_items, max_weight, max_fragile, list_items=items
        batoh=Knapsack(max_weight,max_items,max_fragile)
        matrix_items = (batoh.make_matrix(list_items))
        list = (batoh.choose_items(matrix_items, list_items))
        self.my_packed_bag=list
        saver = datasaver(list)
        saver.save_items()

    def show_insides(self):
        try:
            for object in self.my_packed_bag:
                self.final_sum += object.getvalue()
            print(self.final_sum,"<final sum of backpack    number of items>",len(self.my_packed_bag))
        except:
            print("Still not packed")





if __name__ =='__main__':
    items=itemloader("new items.txt")
    my_bag=PackedKnapsack()
    my_bag.pack_my_bag(items.load_data())
    my_bag.show_insides()












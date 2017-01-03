# equ_volume = []
# equ_price = []
step = 2
door_score = 0.15     #个体趋势误差容忍
percentage_level = 0.6   #总体趋势误差容忍
# total_length =0
class Analyze:
	# global equ_volume
	# global equ_price
	global step
	global door_score
	global percentage_level
	# global total_length 
	def __init__(self,equ_v=[],equ_p=[],step_num=2):
		self.equ_price = equ_p
		self.equ_volume = equ_v
		step = step_num
		self.total_length = len(self.equ_price)
        
	def get_parameters(self,):
		return (step,door_score,percentage_level)
	
	def get_final_percentage_result(self):
		temp_len = len(self.equ_price) - step
		temp_trending = float(self.get_trending())
		print "temp_trending ,temp_len,temp_trending/temp_len,percentage_level",temp_trending ,temp_len,temp_trending/temp_len,percentage_level
		if (temp_trending/temp_len)>=percentage_level:
			return True
		else:
			return 	False
			
	def set_percentage_level(self,score):
		percentage_level = score
		
	def set_door_score(self,score):
		door_score = score
		
	#检查数据数量是否符合要求	
	def check_data_useable(self,):
		if len(self.equ_price) != len(self.equ_volume):
			return False
		else:
			return True
	
	#检查交易量
	def check_volume_score(self,num):
		if self.equ_volume[num]==0:
			return 0 
		else:
                        # print "==",(self.equ_price[num+step]-self.equ_price[num])/self.equ_price[num],"=="
			return (self.equ_volume[num+step]-self.equ_volume[num])/self.equ_volume[num]
			
	#检查价格	
	def check_price_score(self,num): 
		if self.equ_price[num]==0:
			return 0
		else:
			return (self.equ_price[num+step]-self.equ_price[num])/self.equ_price[num]
			
	#开始计算总体趋势
	def get_trending(self):
		#total_length = len(equ_price)
		total_scores = 0
		count = 0
		self.total_length = self.total_length - step -1
		# print "total_length - step",self.total_length , step
		while count<=self.total_length:
			temp_price = self.check_price_score(count)
			temp_volume = self.check_volume_score(count)
			sub_result = abs(temp_price-temp_volume)
			# print "((((",sub_result,count 
			if sub_result <= door_score:
				total_scores = total_scores + 1
			count = count +1
		return total_scores
		
		
		
		
		
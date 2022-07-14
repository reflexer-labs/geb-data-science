from decimal import Decimal

WAD = 1E18
RAY = 1E27
class Rai():
    def __init__(self, redemption_price, redemption_rate, last_update_time,
                 kp, ki, alpha, prop_term=0, integral_term=0):
        
        self.redemption_price = redemption_price
        self.redemption_rate = redemption_rate
        self.last_update_time = last_update_time
        
        self.kp = kp # WAD
        self.ki = ki # WAD
        self.alpha = alpha # RAY
        self.integral_term = integral_term # RAY
        self.prop_term = prop_term # RAY
        
        self.ki_rate = None
        self.kp_rate = None
        
        self.rate_lower_bound = 999999934241503702775225172
        self.rate_upper_bound = 1000000065758500621404894451 
           
    def update_rp(self, time_since):
        self.redemption_price = Decimal(self.redemption_price) * (Decimal(self.redemption_rate)/Decimal(RAY))**time_since
        
    def process(self, market_price, ts):
        # Parameters:
        # Error: RAY
        # Time_since: secs
        
        # Returns
        # pRate: Ray
        # iRate: Ray
        # rp: float
        
        time_since = ts - self.last_update_time
        
        self.update_rp(time_since)
        
        error = int(((self.redemption_price - Decimal(market_price))/self.redemption_price)* Decimal(RAY))
        
        # computer pRate
        self.kp_rate = self.kp/WAD * error
        
        # calculate new area as a trapezoid
        new_area = (error + self.prop_term) / 2   * time_since
        
        # decay factor for old area
        decay = (Decimal(self.alpha)/Decimal(RAY)) ** Decimal(time_since)
        
        # decay old error
        decayed_sum = self.integral_term * float(decay)
        
        self.integral_term = int(float(decayed_sum + new_area))
        
        # computer iRate
        self.ki_rate = self.ki/WAD * self.integral_term
        
        # set this error as old error to use for next trapezoid
        self.prop_term = error
        self.last_update_time = ts
        

        self.redemption_rate = min(max(1e27 + self.kp_rate + self.ki_rate, self.rate_lower_bound), self.rate_upper_bound)
        
        
        return ts, self.redemption_rate, self.kp_rate, self.ki_rate, self.redemption_price, market_price
    
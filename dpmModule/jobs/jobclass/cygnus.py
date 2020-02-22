from ...kernel import core
from ...kernel.core import VSkillModifier as V
from ...kernel.core import CharacterModifier as MDF
from ...character import characterKernel as ck
from functools import partial

def PhalanxChargeWrapper(vEhc, num1, num2):
    PhalanxCharge = core.DamageSkill("시그너스 팔랑크스", 780, 450 + 18*vEhc.getV(num1, num2), 40 + vEhc.getV(num1, num2), cooltime = 30 * 1000).isV(vEhc, num1, num2).wrap(core.DamageSkillWrapper)
    return PhalanxCharge

class CygnusBlessWrapper(core.BuffSkillWrapper):
    def __init__(self, enhancer, skill_importance, enhance_importance, serverlag = 3, level = 230):
        self.isUpgraded = (level >= 245) 
        self.enhancer = enhancer
        self.skill_importance = skill_importance
        self.enhance_importance = enhance_importance
        
        skill = core.BuffSkill("초월자 시그너스의 축복" if isUpgraded else "여제 시그너스의 축복" , 630, 45000, cooltime = 240*1000).wrap(core.BuffSkillWrapper)
        super(CygnusBlessWrapper, self).__init__(skill)

        self.damage_point = 4 + (enhancer.getV(self.skill_importance, self.enhance_importance))//15
        self.damage_limit = 90
        #interval: 데미지 증가 주기 (모름)
        self.interval = 4
        
        # 업그레이드 상태일경우 해당 스펙 적용
        if self.isUpgraded:
            self.damage_point += 2
            self.damage_limit += 30
            
        self.passedTime = 0
        self.serverlag = serverlag

    def spend_time(self, time):
        if self.onoff:
            self.passedTime += time
        super(CygnusBlessWrapper, self).spend_time(time)

    def get_modifier(self):
        
        if self.onoff:
            return core.CharacterModifier(pdamage = min(enhancer.getV(self.skill_importance, self.enhance_importance) + self.damage_point * (self.passedTime // ((self.interval + self.serverlag) * 1000)), self.damage_limit))
        else:
            return core.CharacterModifier()
        
    def _use(self, rem = 0, red = 0):
        self.passedTime = 0
        return super(CygnusBlessWrapper, self)._use(rem = rem, red = red)
---
up:
  - "[[../moc/work|work]]"
---
[moc 其他集成测试](../moc/moc%20其他集成测试.md)
#ed 
![[Pasted image 20240229154500.png|750]]
![[Pasted image 20240229154513.png|725]]
1、图 2.1、图 2.2 构成了传感器发光管的 PWM 驱动电路，
经过阻容滤波电路、同向放大电路后输出直流信号 OUTA，OUTA 连接至图 2.2 中三极管基极端，驱动传感器发光管发光；
2、图 2.1 所示电路为 PWM 控制电路的核心部分。该电路对 PWM 控制信号进行低通滤波及放大，使其转换为幅值与 PWM 占空比相对应的直流电压信号
![[Pasted image 20240229154651.png]]
3、图2.3所示等效电路中电阻 R213、R220、电容 C234、C235构成二阶低通滤波器，经过滤波后 PWM 信号变成带有纹波的直流电压，该电压与 PWM 的占空比成正比
直流电压经过负反馈放大电路提高了电压的驱动能力，形成合适的电压信号控制发光管电路。


PWM 信号经过二阶低通滤波电路，即可得到稳定的直流电压信号。通过调节 PWM 信号的占空比，就可以线性的改变直流电压信号的幅值，从而实现对发光管电流的调整，改变发光管的亮度。这也就是 PWM 调节发光管亮度的基本原理
# 步进电机

在非超载的情况下，电机的转速、停止的位置只取决于脉冲信号的频率和脉冲数，而不受负载变化的影响.
当步进驱动器接收到一个脉冲信号，它就驱动步进电机按设定的方向转动一个固定的角度，称为“步距角”
相数是指电机内部的线圈组数，电机相数不同，其步距角也不同
![[Pasted image 20240229155147.png]]

# 0
## 有pwm
![[Pasted image 20240312160839.png]]
![[Pasted image 20240312160853.png]]
单通道模拟多路复用器
![[Pasted image 20240312183049.png]]
![[Pasted image 20240312160915.png]]
![[Pasted image 20240312160946.png]]
![[Pasted image 20240312181819.png]]
ad 转换器
![[Pasted image 20240312182340.png]]
## 无 pwm
![[Pasted image 20240312161107.png]]
![[Pasted image 20240312161117.png]]
![[Pasted image 20240312161133.png]]
![[Pasted image 20240312161150.png]]
![[Pasted image 20240312161219.png]]

# 传感器校验 
==通过重新设置发光管 PWM **将接收到的电压值**调节到合理的范围内==。
## 光电传感器原理
光电传感器硬件原理如下图所示，分为发射端和接收端，发射端为一个发光二极管，接收端为一个光电三极管，发射端发出的光照射到接收端的三极管上，进而影响三极管的电压输出。发射端发光强度改变，接收端输出的电压也随之改变。
三极管的工作区域分为截止区、放大区和饱和区，**工作在饱和区时，输出电压较稳定。我们对传感器进行 PWM 校验的目的，是找到一个合适的发射端发光强度，在该发光强度下使三极管工作在饱和区，从而得到一个稳定的接收端输出电压**。
具体实现方式为根据对传感器的测试结果设置一合适的输出电压值作为目标值，然后通过对发射端 PWM 进行调节，同时采集输出电压，当输出电压接近目标值时，则将此时的 PWM 值作为发射端的工作 PWM。
![[Pasted image 20240430112423.png]]
![[Pasted image 20240430112435.png]]
# 代码
# 传感器校验日志
SensorPwmVerify 通道传感器 pwm 校验
	DEBUG_LOG_INFO (DEBUG_LOG_SENSOR, ("SensorPwmVerify: CorrMode: %d\n", CorrMode));
	SensorPwmCorrParaInit初始化 pwm 参数
		DEBUG_LOG_INFO (DEBUG_LOG_SENSOR, ("SensorPwmVerify:%s, PwmBefore:%d, PwmRange:%d~%d\n",
		SensorGetName (ptSnsCorrManagerTbl[SnsIdCnt]->mIdManager. mSensorId),
		ptPwmBak[SnsIdCnt], ptPwmCorrPara->mCorrDataRecord. mLesser. mPwm, ptPwmCorrPara->mCorrDataRecord. mBigger. mPwm));
	CurrentAD = SensorCorrGetMaxADProbability
	(ptSnsCorrManagerTbl[SnsIdCnt]);获取传感器校正最大概率AD值
	DEBUG_LOG_INFO (DEBUG_LOG_SENSOR, ("SnsCorr:Data:%s:%d,%d\n",
	SensorGetName (ptSnsCorrManagerTbl[SnsIdCnt]->mIdManager. mSensorId),
	ptSnsCorrManagerTbl[SnsIdCnt]->mCorrPara. mPwmCorr. mPwmUse, CurrentAD));
	SensorPwmCorrPwmChangeCalc 传感器PWM校正PWM更改
		DEBUG_LOG_INFO (DEBUG_LOG_SENSOR, ("SnsData:%s:Pwm:%d, Max:%d, Tar:%d, B:%d,%d,%d, L:%d,%d,%d\n",
		SensorGetName (SnsId),
		ptPwmCorrPara->mPwmUse, CurrentAD, PwmTarVal,
		ptPwmCorrPara->mCorrDataRecord. mBigger. mData,
		ptPwmCorrPara->mCorrDataRecord. mBigger. mPwm,
		ptPwmCorrPara->mCorrDataRecord. mBigger. mUseFlg,
		ptPwmCorrPara->mCorrDataRecord. mLesser. mData,
		ptPwmCorrPara->mCorrDataRecord. mLesser. mPwm,
		ptPwmCorrPara->mCorrDataRecord. mLesser. mUseFlg));
		}
	SensorPwmCorrResHandle 传感器 PWM 校正结果处理
		DEBUG_LOG_INFO (DEBUG_LOG_SENSOR, ("SnsCorr: PwmcorrectSucc. Sensor:%s, Tar:%d, pwm:%d->%d (%d), pwmref:%d, Refresh:%d\n",
		SensorGetName (ptManager->mIdManager. mSensorId),
		PwmTarVal,
		ptPwmBak[SnsIdCnt],
		ptManager->mParaConfig. mPwm,
		STD_ABS (ptPwmBak[SnsIdCnt], ptManager->mParaConfig. mPwm),
		ptManager->mCorrPara. mPwmCorr. mSensorPwmRef,
		PwmRefreshFlg));
	SensorPwmCorrResRefresh 传感器PWM校正结果刷新
		DEBUG_LOG_INFO (DEBUG_LOG_SENSOR, ("SnsCorr:Ad:%s, Pwm:%d, AD:%d\n",
		SensorGetName (ptSnsCorrManagerTbl[SnsIdCnt]->mIdManager. mSensorId),
		ptSnsCorrManagerTbl[SnsIdCnt]->mParaConfig. mPwm,
		AppSensorGetAd (ptSnsCorrManagerTbl[SnsIdCnt]->mIdManager. mSensorId)));
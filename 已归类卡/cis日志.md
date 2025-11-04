---
up:
  - "[[mocWorkCode]]"
---
#kan
#ed 
## 上电
cis 数据格式化
一部分传感器是从 ee 加载的
电机初始化
FlwFSMStat: FLOW_STATE_POWER_ON, GateFSMStat: IDLE 流程开始
cis 自动校正开始
FlwFSMStat: FLOW_STATE_SELFTEST, GateFSMStat:IDLE
cis 偏移量校正
加载上下部 fpga 和 scb
FlwFSMStat: FLOW_STATE_SELFEND, GateFSMStat:IDLE
更新通道传感器的阈值
Cis: 0, Color: 0, MaxValue: 32323, MinValue: 32323, Ref: 24162, Light: 70  
	单个 cis 发光时间校正数据计算过程 
SensorPwmVerify: CorrMode: 0
	传感器校验
FlwFSMStat: FLOW_STATE_WAIT_INIT_CMD, GateFSMStat:IDLE
白基准发光校正
CisAutoCorrectEnd
## 初始化
纸币基准值初始化
鉴伪字典初始化
bv 币种设置
FlwFSMStat: FLOW_STATE_INIT, GateFSMStat:IDLE
传感器校验 
排错流程
BVFSMStat: BV_STATE_Light 
CisAutoCorrectStart
CisAutoCorrectEnd
BVFSMStat:BV_STATE_IDLE
## 入朝
`*******************FlowControlStart\********************`
FlwFSMStat:FLOW_TRANS_STATE_INIT
GateManagerCtrl: Msg Send, MAKERDY
GateManager: MakeGateReady, 3 b 531 d 9 c
GateManagerFsm:READY
GateHandle: RCB_B 1, FsmChg: IDLE->READYING
RcbInit: RCB_B 1 Stage 1 Space check not Start
FlwFSMStat:FLOW_TRANS_STATE_WAIT
BVFSMStat:BV_STATE_PREPARE
BvStart
CisAutoCorrectStart 
RcbInit: RCB_B 1 Stage 3 in check Start 
AppMotorCtrl: MsgSendSucc, RBDM 1, Mode: START, Dir: 0, Speed:500
## 校正
### 偏移
CalcDataForOffset(pCis1Image->mHighDpiWhite.mSrc.pStartAddr,&sCorrectOffsetValue[DEV_CIS_ID_1].mGray);
//计算出来放到 mgray
CisCorrectOffsetCalcResult
//mgray 与 mset 比较，更改的是 mset




DEBUG_LOG_INFO (DEBUG_LOG_CIS, ("Cis 1 OffsetStaticValue:Max:%d, Min:%d\n",
									sCorrectOffsetValue[DEV_CIS_ID_1]. mGray. mMax,
									sCorrectOffsetValue[DEV_CIS_ID_1]. mGray. mMin));

DEBUG_LOG_INFO(DEBUG_LOG_CIS,("**Cis1OffsetCalc**:0x%02x\n",sCorrectOffsetValue[DEV_CIS_ID_1].mSet.mCurValue));

Cis 1 OffsetStaticValueStep:Max: 21, Min:0

DEBUG_LOG_INFO(DEBUG_LOG_CIS,("Cis1OffsetEnd:0x%02x\n",sCorrectOffsetValue[DEV_CIS_ID_1].mSet.mCurValue));
### 暗校正
CisDarkStdRef, retry: 0 //3 次校正如果是 0 就一次过
Cis 0, Dark: 13  Cis 1, Dark:12
CisDarkLast, Id: 0, StdRef: 3188, Current: 3353, retry:0
```
DEBUG_LOG_INFO(DEBUG_LOG_CIS,("Cis0,Dark:%dCis1,Dark:%d\n",
							(sCorrectDarkAverage[DEV_CIS_ID_1]>>8),(sCorrectDarkAverage[DEV_CIS_ID_2]>>8)));
```
###  发光校正
#### CisLightCorrectRGBBalanceStart
CisLightCorrectRGBBalanceInit(CIS_LIGHT_COLOR_W_R);
Result=**CisLightCorrectStdProc**(DevId,pResult,**CORRECT_MODE_R_G_B**);

CisLightCorrectRGBBalanceInit (CIS_LIGHT_COLOR_W_G);
Result=CisLightCorrectStdProc (DevId, pResult, CORRECT_MODE_R_G_B);
#### CisLightCorrectRGB/IRStart
cis01:01
**CisLightCorrect** (DevId, pResult, **CORRECT_MODE_RGBIR**);//引用 CisLightCorrectStdProc

RGB  iR 两个颜色
DEBUG_LOG_TRACE(DEBUG_LOG_CIS,("Cis:%01d,Color:%01d,MaxValue:%01d,MinValue:%01d,Ref:%01d,Light:%01d\n",DevId,CurColor,
		pLight->mStatistic. mMax, pLight->mStatistic. mMin, pLight->mGrayRef. mCurValue, pLight->mSet. mCurValue));
RGB  iR 两个颜色
DEBUG_LOG_TRACE (DEBUG_LOG_CIS, ("CisEx:%01 d, Color:%01 d, MaxValue:%01 d, Ref:%01 d, Light:%01 d\n", DevId, CurColor,
		pLight->mStatistic. mMax, pLight->mGrayRef. mCurValue, pLight->mSet. mCurValue));



DEBUG_LOG_INFO (DEBUG_LOG_CIS, ("Cis 0:RGB:%d, IR:%d, TX 2:%d\n",
				gDevCis[DEV_CIS_ID_1]. mLight[CIS_LIGHT_COLOR_W_R],
				gDevCis[DEV_CIS_ID_1]. mLight[CIS_LIGHT_COLOR_IR 1],
				gDevCis[DEV_CIS_ID_1]. mLight[CIS_LIGHT_COLOR_TXIR 2]));
##### CisLightCorrectDataInit(Mode);
//CisLightCorrectStdProc 下
#### CisLightCorrectUV/TX 1/TX 2/Start
CisLightCorrect (DevId, pResult, **CORRECT_MODE_TXIRUV**)
cis 1   234
cis 2   34
### 白基准校正  
CisLightCorrectBandStart
CisWhiteBandCorrect  白基准校正的初始值

CisWhiteBandCorrectSingle
	CisBandCorrectGetBandInfo
	//CIS 获取白基准坐标位置和灰度数据,起始坐标,长度固定
		CisWhiteBandSearchPosAndValue
		//CIS 白基准位置搜索与灰度统计


```
DEBUG_LOG_INFO(DEBUG_LOG_CIS,("BandStart:%d, RGB:%d-%d, IR:%d-%d, UV:%d-%d, TX1:%d-%d, TX2:%d-%d\n",
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mStartIndex[CORRECT_LIGHT_COLOR_RGB],
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_RGB],
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_RGB]/256,
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_IR],
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_IR]/256,
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_UV],
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_UV]/256,
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_TXIR1],
								   gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_TXIR1]/256,gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_TXIR2],	gDevCis[DEV_CIS_ID_1].mBandInfo.mValue[CORRECT_LIGHT_COLOR_TXIR2]/256
```




```
CisWhiteBandCorrectSaveValue(DEV_CIS_ID_1, CORRECT_LIGHT_COLOR_RGB);
		CisWhiteBandCorrectSaveValue(DEV_CIS_ID_1, CORRECT_LIGHT_COLOR_IR);
		CisWhiteBandCorrectSaveValue(DEV_CIS_ID_1, CORRECT_LIGHT_COLOR_UV);
		CisWhiteBandCorrectSaveValue(DEV_CIS_ID_1, CORRECT_LIGHT_COLOR_TXIR1);
//		CisWhiteBandCorrectSaveValue(DEV_CIS_ID_1, CORRECT_LIGHT_COLOR_TXIR2);


	pData[0] = CisLightCorrectGetImagePointer(CurColor,pCisImage[0]);
	CalcDataForBandLightEx(DevId,pData[0],pData[1],&pLight->mStatistic,pDark);
```

### 明校正
```
	//RGB
	CorrectBrightRefInit(DevId,CORRECT_LIGHT_COLOR_RGB,&sBright[DevId][CORRECT_LIGHT_COLOR_RGB]);
	
CisCorrectBrightDataCalcAndKeep(&gDevCis[DevId].mCorrectFile,pRgb[0],pRgb[1],gDevCis[DevId].mCorrectFile.pDev_bright_rgb,					StartCount,EndCount,&sBright[DevId][CORRECT_LIGHT_COLOR_RGB]);  
	CisCorrectBrightDataFormat(DevId,CORRECT_LIGHT_COLOR_RGB,gDevCis[DevId].mCorrectFile.pDev_bright_rgb); 
```
### 保存数据



## 白基准自动  CisBandCorrectBack
包含偏移量、暗电平、发光时间自校正

if(gCisBandEnable.mLight[CORRECT_LIGHT_COLOR_RGB])
	if (IsCisNeedLightTimeCorrect ())
			**CisLightBandCorrectBackByLight**
				debug (BeforeBandCis)
				debug (afterBandCis)
	CisLightBandCorrectBack
		**CisLightBandCorrectBackByBrightMultiply**
			DEBUG_LOG_TRACE(DEBUG_LOG_CIS,("CisId:%d, Color:%d, Cur:%d-%d, Ref:%d-%d\n",DevId,CurColor,
						   pLight->mStatistic.mMax,
						   (pLight->mStatistic.mMax>>8),
						   BaseValue,
						   (BaseValue>>8)));


IsCisNeedLightTimeCorrect 
	gCisAutoCorrectMode
		true
	else
		if（0）
			IsCisNeedAutoCorrect
		else
			STD_FALSE





## 紫外校正
CisCorrectUvStart...
CisLightCorrectUVStart
CisLightCorrectUv
	CisLightCorrectDataCalc
Cis 0: UV: 117        Cis 1: UV:1
CisLightCorrectUvOK


CisBandCorrectUvStart
CisCorrectUvBrightOK
## 测厚
### 非校正
Thick OK, Channel = 0, Register = 97, BaseValue = 1981, ValueDiff = 64
ThickNoPaper ok, Ave 1981
Thickness Values: 1981,226,2617
ThickAllAverage: 1041, ratio: 1762, cashresult: 0 x 3 ffffff, NoAve:1981
PaperId: 9, Thick Times:1131
BVRetInfo, Mode: 0, PaperId: 9, BvPaperId: 9, sn:??????????, Double: 1, Angle: 2, BnType: 0, Fake: 0, Bn: 254, Index: 0, Value: 0, Atm: 499, Sort: 499, Class: 5, FRj: 18, DestGate: 2, HeadNdSN: 5, Hmax: 7, BvLenC: 76, BvLenS: 0, BvRj: 5, Thick:1041
Rej: 5, Ang: 2, Len: 0, LenC: 76, Dis: 0, Reg: 0,0,0, Width: 154, UpAng: 3, DownAng: 3, Thick:1041


DEBUG_LOG_INFO (DEBUG_LOG_THICK, ("ThickNoPaper ok, Ave%d\n",	gThickSort. mPaper. mChannel[Channel]. mNoCashAverage));	
### 校正
Thick OK, Channel = 0, Register = 97, BaseValue = 1978, ValueDiff = 80
Rej: 0, Ang: 0, Len: 0, LenC: 0, Dis: 0, Reg: 0,0,0, Width: 0, UpAng: 0, DownAng: 0, Thick:0
PaperId: 8, Index: 8, Thick Enter
Paper's Correct Is Ok ,Channel = 0, Amplitude = 581
PaperId: 8, Thick Times:1961425



# 钞间距

c

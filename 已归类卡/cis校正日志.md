---
up:
  - "[[cis代码]]"
---



CisCorrectMain (IsSaveData,\*pResult)


```
CisAppCisStart
CisLightDataGhost//发光时间备份

CisCorrectEnable(STD_FLASE)


if (IsSaveData)
	QspiFlashErase
	CisCorrectFileSave(DEV_CIS_ID_1);
	

CisResult=CisCorrectBright(DevId);//图像明校正,均匀性系数
if(ERR_NO_ERROR!=CisResult)
{
	gDevCis[DEV_CIS_ID_1].mCorrectResult.mStatus=CIS_CORRECT_ERR_BRIGHT;
	gDevCis[DEV_CIS_ID_2].mCorrectResult.mStatus=CIS_CORRECT_ERR_BRIGHT;
	DEBUG_LOG_ERR(DEBUG_LOG_CIS,("CisCorrectBrightFail\n"));
	CisCorrectEnable(DEV_CIS_ID_MAX,STD_TRUE);
	CisLightDataBack(DEV_CIS_ID_MAX);
	returnERR_FAIL;
}



CisCorrectEnable(STD_TRUE)
	
```

# CisAppCisStart

CisScanDefaultLineCountUpdate(CIS_SCAN_LINE_DEFAULT)//扫描行周期SI默认值调整,根据电机速度修正
DevCisReset

## CisScanDefaultLineCountUpdate 
**gScanLineClkCount** =
## DevCisReset
\*FPGA_CIS_RESET_REG =
Wm8233Init(WM_8233_INIT_MODE_RESET);
Wm8233LedTest//CIS扫描测试初始化
### Wm8233Init
DevCisSetSiWidth(gScanLineClkCount);
DevCisOffsetSet(DEV_CIS_ID_1,gDevCis[DEV_CIS_ID_1].mChannel[0].mOffset);
CisLightReset(DEV_CIS_ID_MAX);
#### DevCisSetSiWidth 
\*FPGA_CIS_TGSYNC_TIME = SetWidth;
#### CisLightReset 
```
if(gCisLightSwitch.mLightType==CIS_LIGHTSOURCE_INR)
{
	DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_W_R,1);
	DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_W_G,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_W_R]);
	DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_W_B,1);
}
else
{
	DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_W_R,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_W_R]);
	DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_W_G,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_W_G]);
	DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_W_B,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_W_B]);
}
DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_IR1,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_IR1]);
DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_UV,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_UV]);
DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_TXIR1,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_TXIR2]);	
DevCisLightSet(DEV_CIS_ID_1,CIS_LIGHT_COLOR_TXIR2,gDevCis[DEV_CIS_ID_1].mLight[CIS_LIGHT_COLOR_TXIR1]);


DevCisLightOn(DevId);
```

##### DevCisLightOn 
DevCisClose (DEV_CIS_ID_MAX);
Wm8233LightValueWriteToHardware (DEV_CIS_ID_1);
DevCisOpen (DEV_CIS_ID_MAX);

## CisWhiteBandCorrect
TimerDelayMiliSecond(50);//红外预热
CisScanXLength((CORRECT_ROWS_NEED_BRIGHT + CORRECT_ROWS_ADD),STD_FALSE,CIS_SCAN_MODE_CORRECT);//扫描一段距离

CisWhiteBandCorrectSingle//寻找白基准位置


//保存16位白基准数据
CisScanXLength((CORRECT_ROWS_NEED_LIGHT + CORRECT_ROWS_ADD),STD_FALSE,CIS_SCAN_MODE_CORRECT_CIS1)
CisWhiteBandCorrectSaveValue(DEV_CIS_ID_2, CORRECT_LIGHT_COLOR_RGB);
### CisScanXLength
DevCisImageInit(&sTestCisImage[DEV_CIS_ID_1],DEV_CIS_ID_1);

AppMotorStart(MOTOR_UMBM1, MOTOR_DIR_FORWARD, 400);
if (CIS_SCAN_MODE_CORRECT == Mode
			|| CIS_SCAN_MODE_CORRECT_CIS1 == Mode
			|| CIS_SCAN_MODE_CORRECT_CIS2 == Mode)
{
	DevCisBnImageUpdateStartAddrCorrect(&==<span style="background:#d4b106">sTestCisImage</span>==[DEV_CIS_ID_1],DEV_CIS_ID_1,0);
	CisScanWaitXLengthEnd(DevId,Length \*CIS_SCAN_COLOR_INDEX_MAX + 16 * CIS_SCAN_COLOR_INDEX_MAX)
	DevCisBnImageUpdateEndAddrCorrect(&sTestCisImage[DEV_CIS_ID_1],DEV_CIS_ID_1,0);
}
else
	
AppMotorBrake(MOTOR_UMBM1);
FpgaStopCisDataOutToMemory(DEV_CIS_ID_MAX);
#### DevCisImageInit（\*pBn）
memcpy((void*)pBn,&==<span style="background:#d4b106">gDevCis[DevId].mImage</span>==,sizeof(gDevCis[DevId].mImage));
##### DevCisImageMemoryInit
//White 200DPI
<span style="background:#d2cbff">DataBaseAddrSet</span>(&gDevCis[DEV_CIS_ID_1].mImage.mHighDpiWhite.<span style="background:#d2cbff">**mBuf**</span>,(U8*)**WHITE_TOP_200_START**,WHITE_TOP_200_SIZE);
DataBaseAddrSet(&gDevCis[DEV_CIS_ID_1].mImage.mHighDpiWhite.**mSrc**,(U8*)**WHITE_TOP_200_START**,WHITE_TOP_200_SIZE);
DataBaseAddrSet(&gDevCis[DEV_CIS_ID_1].mImage.mHighDpiWhite.**mDst**,(U8*)**WHITE_TOP_200_START**,WHITE_TOP_200_SIZE);
#### DevCisBnImageUpdateEndAddrCorrect
DevCisBnImageGenerateMMU(&pBn->mHighDpiWhite);
##### DevCisBnImageGenerateMMU 
pImage->==<span style="background:#d2cbff">mDst.pStartAddr</span>== = (U8*)(<span style="background:#d2cbff">MEM_CIS_MMU_START</span> + (pImage->mBuf.pStartAddr - (U8*)WHITE_TOP_200_START) * 2 + pImage->mSrc.pStartAddr - pImage->mBuf.pStartAddr);
#### DevCisBnImageUpdateStartAddrCorrect （\*pBn）更新校正图像起始地址


LineIndex = <span style="background:#d2cbff">DevCisGetCurrentLines</span>(DevId,CIS_LINES_MODE_200DPI,CORRECT_LIGHT_COLOR_RGB);
PtAddr = (LineIndex) * CIS_LEN_DOT_HIGHDPI_EX;
pBn->mHighDpiWhite.<span style="background:#d2cbff">mSrc.pStartAddr</span> = pBn->mHighDpiWhite.**==mBuf==**.pStartAddr + PtAddr;

##### DevCisGetCurrentLines 返回图像扫描索引
if (CIS_LINES_MODE_200DPI == Mode)
{
	Length = \*(volatile U32*)CisLineOffsetDotTableOf200Dpi\[DevId][LightColor];  
	Length = (Length>>10);
}
else
{
	Length = \*(volatile U32*)CisLineOffsetDotTableOf50Dpi\[DevId][LightColor];
	Length = (Length>>8);
}
###### CisLineOffsetDotTableOf200Dpi
```
const volatile U32 *CisLineOffsetDotTableOf200Dpi[DEV_CIS_ID_MAX][8] =
{
	{FPGA_CIS1_BASE_OFFSET_HIGH_0,FPGA_CIS1_BASE_OFFSET_HIGH_1,
	FPGA_CIS1_BASE_OFFSET_HIGH_4,FPGA_CIS1_BASE_OFFSET_HIGH_2,
	FPGA_CIS1_BASE_OFFSET_HIGH_3,FPGA_CIS1_BASE_OFFSET_HIGH_5,
	FPGA_CIS1_BASE_OFFSET_HIGH_6,FPGA_CIS1_BASE_OFFSET_HIGH_7},
	
	{FPGA_CIS2_BASE_OFFSET_HIGH_0,FPGA_CIS2_BASE_OFFSET_HIGH_1,
	FPGA_CIS2_BASE_OFFSET_HIGH_4,FPGA_CIS2_BASE_OFFSET_HIGH_2,
	FPGA_CIS2_BASE_OFFSET_HIGH_3,FPGA_CIS2_BASE_OFFSET_HIGH_5,
	FPGA_CIS2_BASE_OFFSET_HIGH_6,FPGA_CIS2_BASE_OFFSET_HIGH_7},
};
```
#### CisScanWaitXLengthEnd 等待扫描指定长度数据完成
DevCisGetTotalLines(DEV_CIS_ID_2, &TotalLength[0]);
while
	DevCisGetTotalLines(DEV_CIS_ID_2, &TotalLength[1]);
	if (TotalLength[1] > TotalLength[0]
	   && STD_ABS(TotalLength[1],TotalLength[0]) >= XLength)
	{
		break;//启动数据更新成功，丢掉初始数据
	}

##### DevCisGetTotalLines  返回图像扫描索引

for(Cnt=0; Cnt<CIS_TOTAL_LEN_RETRY_MAX; Cnt++)
	engthLsb[Cnt] = \*FPGA_CIS2_LINE_TOTAL_LSB;
	==LengthMsb[Cnt] = \*FPGA_CIS2_LINE_TOTAL_MSB;==
	LengthLast[Cnt] = (LengthLsb[Cnt] | (LengthMsb[Cnt] << 32));
	if(Cnt > 1)
	{
		if(LengthLast[Cnt] == LengthLast[Cnt-1])
		{
			\*pTotal = LengthLast[Cnt];
			break;
		}
	}


# CisCorretRealTimeDark
CisCorretRealTimeDarkSingle
	CisDarkDataCorrect(DEV_CIS_ID_2,gDevCis[DEV_CIS_ID_2].==mCorrectFile==.pDev_dark)

CisDarkDataCorrect
	OriData = CalcAverageMasskMsbLsb
	==\*(pblack + PointCount) = OriData;==



# CisLightCorrect
# CisWhiteBandCorrect

## CisWhiteBandCorrectSingle  寻找白基准位置
CisBandCorrectGetBandInfo(DevId,pData->mSrc.pStartAddr,&==StartPos==, &==BandValue==)   CIS获取白基准坐标位置和灰度数据,起始坐标

gDevCis[DevId].mBandInfo.mStartIndex[CurColor] = ==StartPos==;
gDevCis[DevId].mBandInfo.mEndIndex[CurColor] = StartPos + CIS_BAND_LEN_COUNT;
gDevCis[DevId].mBandInfo.mPga[CurColor] = 0;
gDevCis[DevId].mBandInfo.mValue[CurColor] = ==BandValue==;
### CisBandCorrectGetBandInfo(const U8 DevId, U8 *pAddr, U16* pPos, U16* pValue)
CisWhiteBandSearchPosAndValue(pAddr,**pPos**,**pValue**);
# CisCorrectBright
CisLightResetHeat(DEV_CIS_ID_MAX);
TimerDelayMiliSecond(50);//红外预热	
CisLightReset(DEV_CIS_ID_MAX);
	
CisScanXLength((CORRECT_ROWS_NEED_BRIGHT + CORRECT_ROWS_ADD),STD_TRUE,CIS_SCAN_MODE_CORRECT_CIS1);
CisBrightDataCorrectSingle(DEV_CIS_ID_1)
CisAppCisStop();
## CisBrightDataCorrectSingle
pCisImage[0] = CisScanGetImagePt(DevId);
pRgb[0] = CisLightCorrectGetImagePointer(CORRECT_LIGHT_COLOR_RGB,pCisImage[0]);
ptx1[0] = CisLightCorrectGetImagePointer(CORRECT_LIGHT_COLOR_TXIR1,pCisImage[0]);

CisCorrectBrightDataReserveInit(&gDevCis[DevId].mCorrectFile,StartCount,EndCount);//CIS明校正保留区域初始化(设置为0)

//RGB
CorrectBrightRefInit(DevId,CORRECT_LIGHT_COLOR_RGB,&sBright\[DevId][CORRECT_LIGHT_COLOR_RGB]);//CIS2明校正数据参考基准初始化
CisCorrectBrightDataCalcAndKeep(&gDevCis[DevId].mCorrectFile,pRgb[0],pRgb[1],gDevCis[DevId].mCorrectFile.**pDev_bright_rgb**,
									StartCount,EndCount,&sBright[DevId][CORRECT_LIGHT_COLOR_RGB]);//CIS根据图像数据和标准计算明校正
CisCorrectBrightEdgeDeal(ptx1[0],gDevCis[DevId].mCorrectFile.**==pDev_bright_rgb==**,StartCount,EndCount)
CisCorrectBrightDataFormat(DevId,CORRECT_LIGHT_COLOR_RGB,gDevCis[DevId].mCorrectFile.**pDev_bright_rgb**);将明校正数据写入到FPGA对应地址中

### CisLightCorrectGetImagePointer (\*pImage)
pAddr = &pImage->mHighDpiWhite;
return pAddr
### CisCorrectBrightDataCalcAndKeep (CIS_CORRECT_FILE_T \*pFile, CIS_IMAGE_BASE_T \*pMsb, CIS_IMAGE_BASE_T \*pLsb, U16 \*pbright, U16 start_count, U16 end_count, CORRECT_BRIGHT_T \*pRef)

```
for (start_count,end_count)
	DataBright = CalcAverageMaskMsbLsb(pMsb->mSrc.pStartAddr + OffCount + PointCount, 
										   pLsb->mSrc.pStartAddr + OffCount + PointCount,
										   CORRECT_ROWS_NEED_BRIGHT, CIS_LEN_DOT_HIGHDPI_EX, 
										   (U32)(pMsb->mBuf.pStartAddr + pMsb->mBuf.mSize - 1),
										   (U32)(pLsb->mBuf.pStartAddr + pLsb->mBuf.mSize - 1));
	DataBright &= 0xFFF0;
	DarkData = \*(pFile->pDev_dark + PointCount);
	if (DataBright > DarkData)
	{
		DataBright -= DarkData;
	}
	DataBright = STD_MAX_MIN_LIMIT(DataBright,(pRef->mGray.mHighRef<<8),(pRef->mGray.mLowRef<<8));//取极大值极小值区间内的数;
	BrightBase = ((pRef->mRef<<8) * pRef->mMutiply)/DataBright;//最高亮度 * 明校正扩大系数 / 对应点灰度
	\*(pbright + PointCount) = (U16)BrightBase;
```
#### ==CalcAverageMaskMsbLsb==（\*pMsb,\*pLsb,num,step,MsbMask,LsbMask）
* @param [in]  const U8* addr 数据地址
* @param [in]  const U16 num  计算数量
* @param [in]  U16 step       数据增量
* @param [in]  U132 mask   环形缓冲区掩码, 指针转圈用


for (pt_index = 0; pt_index < num; pt_index++ )
{
	DataMsb = \*(U8\*)((U32)(pMsb + (pt_index * step)) &  MsbMask);	//灰度数据
	DataLsb = \*(U8\*)((U32)(pLsb + (pt_index* step)) &  LsbMask);	//灰度数据	
	DarkData = ((DataMsb<<8) | DataLsb);						
	DarkData &= 0xFFF0;
	sum += DarkData;
}

return((sum / num) & 0x0000FFFF);			   //返回平均值

### CisCorrectBrightDataFormat



# 总结 
## mDst
是内存映射后的

ImageRecognitionSort//图像识别清分
	init_image（CisImage->mLowDpiWhite.mDst.pStartAddr）
	SortRefGetBaseValue(ImgPara,CisImage->mLowDpiWhite.mDst.pStartAddr,gImageVsCisIdTable[ImageType],CORRECT_LIGHT_COLOR_RGB);//计算红外图像的基准值


SerialNoOcrGetImageAndSendToLinux 图像冠子号识别数据准备
	pOcrPara->image_ir_50dpi[0] = UpCisScanData->mCisImageRotate. mLowDpiIr. mDst. pStartAddr;
	'
	
# mbuf 
DevCisImageFpgaInit
	\*FPGA_CIS1_BASE_ADDR_LOW_1 = (U32)gDevCis[DEV_CIS_ID_1].mImage.mLowDpiIr.mBuf.pStartAddr;

CalcDataForLightDark
```
//计算单输出图像灰度直方图
	CalcHistogramFromRectMemDarkExMask(pData->mSrc.pStartAddr,pDark,CORRECT_ROWS_START,CORRECT_ROWS_NEED_LIGHT,
										   CORRECT_DATA_LIGHT_START,CORRECT_DATA_LIGHT_END,1,(U32)(pData->mBuf.pStartAddr + pData->mBuf.mSize - 1),
										   sGrayHist); 
```


 CisDarkDataCorrect
```
CalcAverageMaskMsbLsb(pMsb->mSrc.pStartAddr + OffCount + PointCount,
									pLsb->mSrc.pStartAddr + OffCount + PointCount, 
									CORRECT_ROWS_NEED_BLACK,
									CIS_LEN_DOT_HIGHDPI_EX, 
									(U32)(pMsb->mBuf.pStartAddr + pMsb->mBuf.mSize - 1),
									(U32)(pLsb->mBuf.pStartAddr + pLsb->mBuf.mSize - 1));
```



CisCorrectBrightDataCalcAndKeep //CIS根据图像数据和标准计算明校正
```
CalcAverageMaskMsbLsb(pMsb->mSrc.pStartAddr + OffCount + PointCount, 
									   pLsb->mSrc.pStartAddr + OffCount + PointCount,
									   CORRECT_ROWS_NEED_BRIGHT, CIS_LEN_DOT_HIGHDPI_EX, 
									   (U32)(pMsb->mBuf.pStartAddr + pMsb->mBuf.mSize - 1),
									   (U32)(pLsb->mBuf.pStartAddr + pLsb->mBuf.mSize - 1));
```




CalcDataForBandLightEx//白基准发光校正数据统计，去除暗校正
	CalcAverageMaskMsbLsb


GetCisScanData
	case 0x00:
		StartAddr = pImag->mHighDpiWhite.mBuf.pStartAddr;
		\*DataSize = 32 * 1024 * 1024;
# msrc 
是buf加上偏移（当前扫描行），
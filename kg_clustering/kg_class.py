'''
The functions inside of kg_class compute the classes in the KG model

-----------------------
Requirements/Variables
-----------------------
All the outputs from data_prep

BE: This appears as input of some functions, and is the whole class B and E combined - BE = ET+EF+BS+BW

---------
Functions
---------
X_loc: Computes the subclass labeled X.
Y_sub: Computes the sub-sub classes of B-D.

'''


def ET_loc(Tmax):
    '''
    Takes Tmax as numpy array to return the locations of ET.
    '''
    ET = np.zeros_like(Tmax)
    ET[(0<=Tmax) & (Tmax<10)] = 1
    
    return ET


def EF_loc(Tmax):
    '''
    Takes Tmax as numpy array to return the locations of EF.
    '''
    EF = np.zeros_like(Tmax)
    EF[Tmax<0] = 1
    
    return EF


def BS_loc(Pann, Pth):
    '''
    Takes Pann and Pth as np arrays to return the locations of BS.
    '''
    BS = np.zeros_like(Pann)
    BS[(5*Pth < Pann) & (Pann < 10*Pth)]=1
    
    return BS



def BW_loc(Pann, Pth):
    '''
    Takes Pann and Pth as np arrays to return the locations of BW.
    '''
    BW = np.zeros_like(Pann)
    BW[(5*Pth >= Pann)]=1
    
    return BW


def AF_loc(Tmin, Pmin, BE):
    '''
    Takes Tmin and Pmin to as np arrays to return the locations of AF.
    '''
    
    AF = np.zeros_like(Tmin)
    
    #First, select all the possible locations of interest in the A class:
    AF[Tmin>=18] = 1
    #Then, remove locations not in the AF class:
    AF[Pmin<60] = 0
    #Then remove classes B and E:
    AF = AF - BE
    AF[AF<0] = 0
    
    return AF


def AM_loc(Tmin, Pann, Pmin, BE):
    '''
    Takes Tmin, Pann, Pmin, BE as np arrays to return the locations of AM.
    '''
    
    AM = np.zeros_like(Tmin)
    #First, select all the possible locations of interest in the A class:
    AM[Tmin>=18] = 1
    #Then, remove locations not in the AM class:
    AM[Pann<25*(100-Pmin)]=0
    #Then remove classes B and E:
    AM = AM - BE
    AM[AM<0] = 0
    
    
    return AM


def AS_loc(Tmin, Pssum, BE):
    '''
    Takes Tmin and Pmin to as np arrays to return the locations of AS.
    '''   
    
    AS = np.zeros_like(Tmin)
    #First, select all the possible locations of interest in the A class:
    AS[Tmin>=18] = 1
    #Then, remove locations not in the AS class:
    AS[Pssum>=60] = 0
    #Then remove classes B and E:
    AS = AS - BE
    AS[AS<0] = 0
    
    return AS




def AW_loc(Tmin, Pwsum, BE):
    '''
    Takes Tmin and Pmin to as np arrays to return the locations of AW.
    '''   
    
    AW = np.zeros_like(Tmin)
    #First, select all the possible locations of interest in the A class:
    AW[Tmin>=18] = 1
    #Then, remove locations not in the AS class:
    AW[Pwsum>=60] = 0
    #Then remove classes B and E:
    AW = AW - BE
    AW[AW<0] = 0
    
    return AW



def CS_loc(Tmin, Psmin, Pwmin, Pwmax, BE):
    '''
    Takes Tmin, Psmin, Pwmin, Pwmax, BE as np arrays to return the locations of CS.
    '''
    
    CS = np.zeros_like(Tmin)
    #First, select all possible locations of interest in the C class:
    CS[(-3< Tmin) & (Tmin<18)] = 1
    #Then remove locations not in the CS class:
    CS[Psmin>=Pwmin] = 0
    CS[Pwmax<=3*Psmin] = 0
    CS[Psmin>=40] = 0
    #Then remove classes B and E:
    CS = CS - BE
    CS[CS<0] = 0
    
    return CS




def CW_loc(Tmin, Psmin, Pwmin, Psmax, BE):
    '''
    Takes Tmin, Psmin, Pwmin, Psmax, BE as np arrays to return the locations of CW.
    '''
    
    CW = np.zeros_like(Tmin)
    #First, select all possible locations of interest in the C class:
    CW[(-3< Tmin) & (Tmin<18)] = 1
    #Then remove locations not in the CW class:
    CW[Pwmin>=Psmin] = 0
    CW[Psmax<= 10*Pwmin] = 0
    #Then remove classes B and E:
    CW = CW - BE
    CW[CW<0] = 0
    
    
    return CW




def CF_loc(Tmin, CS, CW, BE):
    '''
    Takes Tmin, CS, CW, BE as np arrays to return the locations of CF.
    '''
    CF = np.zeros_like(Tmin)
    #First, select all possible locations of interest in the C class:
    CF[(-3< Tmin) & (Tmin<18)] = 1
    #Remove everything in the CS and CW class:
    CF = CF - CS - CW
    #Then remove classes B and E:
    CF = CF - BE
    CF[CF<0] = 0
    
    
    return CF



def DS_loc(Tmin, Psmin, Pwmin, Pwmax, BE):
    '''
    Takes Tmin, Psmin, Pwmin, Pwmax, BE as np arrays to return the locations of DS.
    '''
    
    DS = np.zeros_like(Tmin)
    #First, select all possible locations of interest in the C class:
    DS[(-3>= Tmin)] = 1
    #Then remove locations not in the CS class:
    DS[Psmin>=Pwmin] = 0
    DS[Pwmax<=3*Psmin] = 0
    DS[Psmin>=40] = 0
    #Then remove classes B and E:
    DS = DS - BE
    DS[DS<0] = 0
    
    return DS





def DW_loc(Tmin, Psmin, Pwmin, Psmax, BE):
    '''
    Takes Tmin, Psmin, Pwmin, Psmax, BE as np arrays to return the locations of DW.
    '''
    
    DW = np.zeros_like(Tmin)
    #First, select all possible locations of interest in the C class:
    DW[(-3>=Tmin)] = 1
    #Then remove locations not in the CW class:
    DW[Pwmin>=Psmin] = 0
    DW[Psmax<= 10*Pwmin] = 0
    #Then remove classes B and E:
    DW = DW - BE
    DW[DW<0] = 0
    
    return DW




def DF_loc(Tmin, DS, DW, BE):
    '''
    Takes Tmin, DS, DW, BE as np arrays to return the locations of DF.
    '''
    DF = np.zeros_like(Tmin)
    #First, select all possible locations of interest in the C class:
    DF[(-3>= Tmin)] = 1
    #Remove everything in the CS and CW class:
    DF = DF - DS - DW
    #Then remove classes B and E:
    DF = DF - BE
    DF[DF<0] = 0
    
    
    return DF


### The following are for finding the sub-sub classes of B-D



def B_sub(B_class, Tmean):
    '''
    This function finds the sub-sub classes within the B sub-classes.
    '''
    #First, we mask out the B subclass on the temperature:
    T_mask = B_class*Tmean
    
    #Next, we create a mask for the two sub-sub-classes:
    h_class = np.zeros_like(T_mask)
    h_class[T_mask>= 18] = 1
    
    k_class = B_class - h_class
    
    return h_class, k_class



def CD_sub(CD_class, Tmax, Tmin, warmsum):
    '''
    Compute sub-sub-classes of the C and D class
    '''
    
    #First, we compute the a class:
    T_max_mask = CD_class*Tmax
    a_class = np.zeros_like(Tmax)
    a_class[T_max_mask>= 22] = 1
    
    #Next we form the b class.  This is done by first selecting all possible points that might be in b_class, and then zeroing out the 
    #points that are not in b_class:
    b_class = CD_class - a_class
    b_class[warmsum<=3] = 0
    
    #Next, we form the c class in the same manor as b class:
    c_class = CD_class - a_class - b_class
    c_class[Tmin>=-38] = 0
    
    #What is left over is d_class
    d_class = CD_class - a_class - b_class - c_class
    
    return a_class, b_class, c_class, d_class


# # Put together to compute class



def KG_model(Tmean, Tmax, Tmin, Pth, Pann, Pmin, Pssum, Pwsum, Psmin, Pwmin, Psmax, Pwmax, warmsum):
    '''
    Computes each of the KG classes, and returns a single array with each point corresponding to a different point in the KG model. 
	The values of KG are integers in [1,31], one for each of the classes.  
	The values are:
	
	1= ET  
	2=EF 
	3=BSh 
	4=BSk 
	5=BWs 
	6=BWk 
	7=CSa 
	8=CSb 
	9=CSc
	10=CWa
	11=CWb
	12=CWc
	13=CFa 
	14=CFb 
	15=CFc 
	16=DSa
	17=DSb
	18=DSc 
	19=DSd 
	20=DWa 
	21=DWb
	22=DWc 
	23=DWd 
	24=DFa 
	25=DFb
	26=DFc 
	27=DFd 
	28=AF 
	29=AM 
	30=AS 
	31=AW
    
    '''
    
    ET = ET_loc(Tmax)
    EF = EF_loc(Tmax)
    
    BS = BS_loc(Pann, Pth)
    BW = BW_loc(Pann, Pth)
    
    #Add together to get BE, which is used to compute the rest of the classes
    BE = ET+EF+BS+BW
    
    AF = AF_loc(Tmin, Pmin, BE)
    AM = AM_loc(Tmin, Pann, Pmin, BE)
    AS = AS_loc(Tmin, Pssum, BE )
    AW = AW_loc(Tmin, Pwsum, BE)
    
    CS = CS_loc(Tmin, Psmin, Pwmin, Pwmax, BE)
    CW = CW_loc(Tmin, Psmin, Pwmin, Psmax, BE)
    CF = CF_loc(Tmin, CS, CW, BE)
    
    DS = DS_loc(Tmin, Psmin, Pwmin, Pwmax, BE)
    DW = DW_loc(Tmin, Psmin, Pwmin, Psmax, BE)
    DF = DF_loc(Tmin, DS, DW, BE)
    
    #Find the sub-classes of B:
    BSh, BSk =  B_sub(BS, Tmean)
    BWs, BWk =  B_sub(BW, Tmean)
    
    #Find the sub classes of C:  Note that CSd is not possible by construction
    CSa, CSb, CSc, CSd = CD_sub(CS, Tmax, Tmin, warmsum)
    CWa, CWb, CWc, CWd = CD_sub(CW, Tmax, Tmin, warmsum)
    CFa, CFb, CFc, CFd = CD_sub(CF, Tmax, Tmin, warmsum)
    
    #Find the sub classes of D:
    DSa, DSb, DSc, DSd = CD_sub(DS, Tmax, Tmin, warmsum)
    DWa, DWb, DWc, DWd = CD_sub(DW, Tmax, Tmin, warmsum)
    DFa, DFb, DFc, DFd = CD_sub(DF, Tmax, Tmin, warmsum)
    
    
    KG = ET + 2*EF + 3*BSh + 4*BSk + 5*BWs + 6*BWk + 7*CSa + 8*CSb + 9*CSc + 10*CWa + 11*CWb + 12*CWc + 13*CFa + 14*CFb + 15*CFc +16*DSa + 17*DSb + 18*DSc +  19*DSd + 20*DWa +21*DWb + 22*DWc + 23*DWd + 24*DFa + 25*DFb + 26*DFc +  27*DFd +  28*AF + 29*AM + 30*AS + 31*AW
    
    return KG
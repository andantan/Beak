from Core.Errors.errors import BeakErrors

from Core.Errors import *
from Data.Errors import *


ERROR_CODE = {
    BeakErrors.UnAuthorizedModuleException.__name__                 :  "BE_01",
    CommonQueueExceptions.ReallocationException.__name__            :  "QE_01",
    CommonQueueExceptions.RequiredAllocationException.__name__      :  "QE_02",
    CommonQueueExceptions.NotAllocatedException.__name__            :  "QE_03",
    CommonQueueExceptions.OutofQueueRangeException.__name__         :  "QE_04",
    CommonQueueExceptions.EndOfQueueException.__name__              :  "QE_05", 
    PrefixQueueExceptions.SaturationOfQueueException.__name__       :  "QE_06",
    InfixQueueExceptions.StillLinedUpInQueueException.__name__      :  "QE_07",
    InfixQueueExceptions.EnteredObjectWhileRefreshing.__name__      :  "QE_08",
    PostfixQueueExceptions.SaturationOfQueueException.__name__      :  "QE_09",
    InfixQueueErrors.InfixQueueAbnormalStatusError.__name__         :  "QE_10",
    AQStatusExceptions.NotAllocatedException.__name__               :  "SE_01",
    VCStatusExceptions.ReallocationException.__name__               :  "SE_02",
    VCStatusExceptions.NotAllocatedException.__name__               :  "SE_03",
    PLStatusExceptions.ReallocationException.__name__               :  "SE_04",
    PLStatusExceptions.NotAllocatedException.__name__               :  "SE_05",
    PLStatusExceptions.NothingInRequiredException.__name__          :  "SE_06",
    VCStatusErrors.DetectedWandererVC.__name__                      :  "SE_07",
    PLStatusErrors.AllocationIncongruityError.__name__              :  "SE_08",
    PLStatusErrors.RequestExhalation.__name__                       :  "SE_09",
    PermissionExceptions.ReallocationException.__name__             :  "PE_01",
    PermissionExceptions.ReRegistrationException.__name__           :  "PE_02",
    PermissionExceptions.RequiredAllocationException.__name__       :  "PE_03",
    MessageStorageExceptions.ReallocationException.__name__         :  "ME_01",
    MessageStorageExceptions.RequiredAllocationException.__name__   :  "ME_02",
    MessageStorageExceptions.NotAllocatedException.__name__         :  "ME_03",
    ContextStorageExceptions.ReallocationException.__name__         :  "CE_01",
    ContextStorageExceptions.RequiredAllocationException.__name__   :  "CE_02",
    ContextStorageExceptions.NotAllocatedException.__name__         :  "CE_03",
    AQHandlerWarnings.FirstAudioWarning.__name__                    :  "HE_01",
    AQHandlerWarnings.LastAudioWarning.__name__                     :  "HE_02",
    AQHandlerWarnings.EndedPlaylistWarning.__name__                 :  "HE_03",
    AQHandlerWarnings.StagingAudioWarning.__name__                  :  "HE_04",
    AQHandlerWarnings.OutofRangeWarning.__name__                    :  "HE_05",
    AQHandlerWarnings.AlreadyPausedWarning.__name__                 :  "HE_06",
    AQHandlerWarnings.AlreadyPlayingWarning.__name__                :  "HE_07",
    AQHandlerWarnings.DeactivatedVoiceClientWarning.__name__        :  "HE_08",
}

HANDERABLE_ERROR_CODE = (
    "QE_05", "QE_06", "QE_09",
    "SE_07",
    "ME_01", "ME_02", "ME_03",
    "CE_01", "CE_02", "CE_03",
    "HE_01", "HE_02", "HE_03",
    "HE_04", "HE_05", "HE_06",
    "HE_07", "HE_08",
)

RISK_ERROR_CODE = (
    "QE_07",
    "QE_08",
    "QE_10",
    "SE_06",
    "SE_08"
)

REQUEST_ERROR_CODE = (
    "SE_09"
)
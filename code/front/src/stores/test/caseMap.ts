import { QuestionLibrary } from './calData'
import { EMRCaseLibrary } from './emrData'

export const CaseMap = {
    "EMR_01": {
        "text": EMRCaseLibrary["EMR_01"],
        "questions": [
            QuestionLibrary["CAL_2"],
            QuestionLibrary["CAL_5"],
            QuestionLibrary["CAL_6"],
        ]
    },
    "EMR_02": {
        "text": EMRCaseLibrary["EMR_02"],
        "questions": [
            QuestionLibrary["CAL_68"],
            QuestionLibrary["CAL_48"],
            QuestionLibrary["CAL_8"],
        ]
    },
    "EMR_03": {
        "text": EMRCaseLibrary["EMR_03"],
        "questions": [
            QuestionLibrary["CAL_48"],
            QuestionLibrary["CAL_15"],
        ]
    },
    "EMR_04": {
        "text": EMRCaseLibrary["EMR_04"],
        "questions": [
            QuestionLibrary["CAL_2"],
            QuestionLibrary["CAL_8"],
        ]
    }
}
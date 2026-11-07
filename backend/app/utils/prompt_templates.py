from app.config.settings import settings
logger = settings.get_logger()


class PromptTemplates:
    """
    Centralized Prompt Repository
    Medical Coding Assistant
    """

    @staticmethod
    def clinical_note_extraction_prompt(
        clinical_note: str
    ) -> str:

        logger.info(
            "Generating Clinical Note Extraction Prompt"
        )

        return f"""
You are an expert Clinical Documentation Specialist.

Your task is to analyze the clinical note and identify:

1. Diagnoses
2. Chronic Conditions
3. Acute Conditions
4. Symptoms
5. Comorbidities

Instructions:
-------------
- Extract only medically relevant conditions.
- Remove duplicate conditions.
- Normalize terminology.
- Return valid JSON only.
- Do not include explanations.

Clinical Note:
--------------
{clinical_note}

Expected JSON:
--------------
{{
    "conditions": [
        "Type 2 Diabetes Mellitus",
        "Hypertension"
    ]
}}
"""

    @staticmethod
    def icd_coding_prompt(
        conditions: list
    ) -> str:

        logger.info(
            "Generating ICD Coding Prompt"
        )

        return f"""
You are a Certified ICD-10 Medical Coding Specialist.

Your task:
----------
Assign the most appropriate ICD-10 code
for each condition.

Instructions:
-------------
- Use ICD-10-CM standards.
- Include code description.
- Include confidence score.
- Confidence score must be between 0 and 1.
- Return JSON only.
- No explanations.

Conditions:
-----------
{conditions}

Expected JSON:
--------------
{{
    "codes": [
        {{
            "diagnosis": "Type 2 Diabetes Mellitus",
            "icd10_code": "E11.9",
            "description": "Type 2 diabetes mellitus without complications",
            "confidence_score": 0.98
        }}
    ]
}}
"""

    @staticmethod
    def validation_prompt(
        conditions: list,
        coding_result: dict
    ) -> str:

        logger.info(
            "Generating Validation Prompt"
        )

        return f"""
You are a Senior Medical Coding Auditor.

Review:
-------
1. Extracted Conditions
2. ICD-10 Mapping
3. Documentation Completeness

Validation Rules:
-----------------
- Verify diagnosis-to-code mapping.
- Identify missing codes.
- Identify unsupported diagnoses.
- Check coding accuracy.
- Check documentation quality.

Conditions:
-----------
{conditions}

Coding Result:
--------------
{coding_result}

Return JSON Only:
-----------------
{{
    "validation_status": "PASS",
    "validation_summary":
    "All diagnoses correctly coded.",
    "missing_conditions": [],
    "incorrect_codes": [],
    "documentation_gaps": []
}}
"""

    @staticmethod
    def coding_audit_prompt(
        clinical_note: str,
        conditions: list,
        coding_result: dict
    ) -> str:

        logger.info(
            "Generating Coding Audit Prompt"
        )

        return f"""
You are a Healthcare Coding Compliance Officer.

Perform a coding audit.

Clinical Note:
--------------
{clinical_note}

Conditions:
-----------
{conditions}

Assigned Codes:
---------------
{coding_result}

Audit Requirements:
-------------------
1. Coding Accuracy
2. Compliance Check
3. Documentation Adequacy
4. Revenue Impact
5. Missing Diagnoses

Return JSON Only:
-----------------
{{
    "audit_score": 95,
    "compliance_status": "COMPLIANT",
    "revenue_risk": "LOW",
    "recommendations": [
        "No additional coding required"
    ]
}}
"""

    @staticmethod
    def medical_summary_prompt(
        conditions: list,
        coding_result: dict
    ) -> str:

        logger.info(
            "Generating Medical Summary Prompt"
        )

        return f"""
You are a Clinical Documentation Specialist.

Create a concise coding summary.

Conditions:
-----------
{conditions}

ICD Coding:
-----------
{coding_result}

Return JSON:
------------
{{
    "summary":
    "Patient diagnosed with Type 2 Diabetes and Hypertension."
}}
"""
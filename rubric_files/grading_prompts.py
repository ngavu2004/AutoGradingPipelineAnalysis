# The prompts including the examples of good and bad submission for each section
from langchain import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
grading_prompts_v1 = {
   "Description":  (PromptTemplate.from_template("""
You are grading a project description. It should  {criteria}. Compare the submission’s Project Description / Purpose with the example with grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

This is an example of a good submission which should have a grade of 100:

"Project Name: Improving Appointment Completion Rates for Publicly Insured Patients
Clinic: Main Street Healthcare Center
Process: Clinic scheduling
TIP 2.0 Process Milestone: Health Equity
Project Description / Purpose:
Patients with public insurance often face barriers to accessing healthcare services, leading to higher rates of missed appointments. This project aims to identify and address these barriers, ensuring that all patients have equitable access to primary care services. The purpose of this project is to increase the percentage of completed primary care appointments among individuals with public insurance, thereby improving access to healthcare and promoting health equity within the patient population."

This is an example of a good submission which should have a grade of 50:

"Project Name: Behavioral Health and HHAC Screening
Clinic: HASS Clinic
Process: Case Management Model: Screening and Levels of Care Referrals
TIP 2.0 Process Milestone: 3: Implement a process for screening for health-related social needs (HRSN) and
connecting members seen to CBOs to address individual social needs.
Project Description / Purpose:
CASS will develop a screening tool to determine clients’ eligibility for services from the Behavioral Health program that includes screening of Social Determinants of Health needs.
"

This is an example of a bad submission which should have a grade of 0 since there is not enough detail:

"This project aims to identify and address these barriers, ensuring that all patients have equitable access to primary care services.”

Grade this submission:
""")),

"Overview": (PromptTemplate.from_template("""
You are grading a project overview. This project description is also provided. It should {criteria}.Compare the submission with the example with a grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

This is an example of a good submission which should have a grade of 100
Project description:
“Patients with public insurance often face barriers to accessing healthcare services, leading to higher rates of missed appointments. This project aims to identify and address these barriers, ensuring that all patients have equitable access to primary care services. The purpose of this project is to increase the percentage of completed primary care appointments among individuals with public insurance, thereby improving access to healthcare and promoting health equity within the patient population.”
Project overview:
“Problem Summary:
Main Street Healthcare has observed a significant performance gap in the completion of primary care appointments among patients with public insurance. Despite efforts to provide high-quality care, Main Street has a high no-show rate and low appointment adherence among this patient group. The current completion rate for primary care appointments among patients with public insurance is 60%, compared to an 85% completion rate among privately insured patients. This 25% performance gap indicates that patients with public insurance are missing crucial primary care visits, which affects their overall health outcomes and the facility's ability to deliver equitable care.
The impact on patients includes unmanaged chronic conditions, delayed diagnosis of new health issues, and inadequate preventive care. Healthcare providers face increased workloads and stress as they attempt to accommodate rescheduled appointments and manage the health complications arising from missed visits. The high no-show rate disrupts clinic operations, leading to inefficiencies, wasted resources, and scheduling difficulties, impacting the overall workflow and morale of the staff.
Desired Outcome(s):
Key Deliverables
Barrier Analysis Report: Detailed analysis of the barriers faced by publicly insured patients in completing appointments.
Intervention Plan: Comprehensive plan outlining the targeted interventions to address identified barriers.
Educational Materials: Culturally and linguistically appropriate educational resources for patients.
Training Programs: Training sessions for staff on the importance of health equity and strategies to improve appointment adherence.
Progress Reports: Regular updates on the progress of the project, including key metrics and feedback from patients and staff.
Project Goal
Increase the percentage of completed primary care appointments among individuals with public insurance by 20% within three months.

Benefits:
Improving completed primary care appointments among patients with public insurance enhances health outcomes through early detection and preventive care, reduces healthcare costs by lowering emergency visits and hospitalizations, and improves patient engagement and satisfaction by fostering trust and continuity of care. It promotes health equity by addressing disparities and ensuring equal access to services, empowers vulnerable populations, and optimizes resource utilization by reducing no-show rates and improving clinic workflow. Additionally, it strengthens community health through better population health management and public health initiatives, creating a more efficient and equitable healthcare system.
”

This is an example of an adequate submission which should have a grade of 50. This submission satisfies the requirements but it is not as detailed as the first submission.
Project Description
“Increasing panel size and coordinated care for the patients that receive care at the clinic is important to improve health outcomes. When the medical providers can review each other’s records through a shared EHR and discuss cases, the patient should have better health outcomes as well as improved understanding of their health conditions.”
Project Overview
“Problem Summary:
There are approximately 700 adult patients receiving psychiatric care in the 4 adult
clinic locations. Of these patients, less than 15% are being treated by on-site primary
care providers (PCP). This causes a gap in providing all-inclusive services and having
access to comorbid conditions through electronic medical record (EMR). 60% of patients that are paneled to psychiatric providers are eligible (insurance) to receive care from PCP.
Desired Outcome(s):
By September 2015, there will be an Increased panel size for integrated providers to 35%
(approximately 1750 patients).
Benefits:
Having shared EMR, availability for coordination of care activities, there will be increased access to care and coordinated service delivery. This will improve patient outcomes and decrease health inequities.”

This is an example of a bad submission which should have a grade of 0 due to lack of detail:
“Problem Summary: Hot weather, increasing number of people getting sick
Desired Outcome(s): Decrease in the number of people getting sick
Benefits: Increase water access for individuals with heat shock”

Grade this submission:

""")),
"Timeline": (PromptTemplate.from_template("""
You are grading a project timeline. It should  {criteria}. Compare the submission with the example with a grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

This is an example of a good submission which should have a grade of 100
"Task 1: Planning and Analysis (Month 1)
Task 2: Intervention Development (Month 2)
Task 3: Implementation (Months 2 and 3)
Task 4: Monitoring and Evaluation (Month 3)
"

This is an example of a bad submission which should have a grade of 0 due to lack of due date:
“Task 1: Planning and Analysis
Task 2: Intervention Development
Task 3: Implementation
Task 4: Monitoring and Evaluation”

Grade this submission:

"""))
}

grading_prompts_v2 = {
    "Milestone": (PromptTemplate.from_template("""
You are grading a project milestone. It should  {criteria}. Compare the submission’s milestone with the example with a grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]


Grade this submission:
{milestone}
""")),

   "Description":  (PromptTemplate.from_template("""
You are grading a project description. It should  {criteria}. Compare the submission’s Project Description / Purpose with the example with grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

Grade this submission:
{description}
""")),

"Overview": (PromptTemplate.from_template("""
You are grading a project overview. This project description is also provided. It should {criteria}.Compare the submission with the example with a grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

Grade this submission:
{overview}
""")),

"Timeline": (PromptTemplate.from_template("""
You are grading a project timeline. It should  {criteria}. Compare the submission with the example with a grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

Grade this submission:
{timeline}
""")),

"Scope": (PromptTemplate.from_template("""
You are grading a project scope. It should {criteria}. Compare the submission with the example with a grade of 100 and the example with a grade of 50. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]
Grade this project scope given its project description:
Project description: {description}
Project scope: {scope}
""")),

"Team": (PromptTemplate.from_template("""
You are grading the project team member part. It should {criteria}. Compare the submission with the example with a grade of 100 and the example with a grade of 0. The highest grade possible is 100 and the lowest grade possible is 0. Output with format: Grade: [grade]. Comment: [comment]

Grade this submission:
{team}
"""))
}

grading_prompts_v4 = PromptTemplate.from_template("""
You are grading a project {section}. This is the criteria: {criteria}. Give the grade in range 0 to 5. If the information specified in
                                               criteria was not provided in the submission, even if the criteria is partially met, grade it 0. If the submission include the information needed in criteria,
                                                grade it 3. If the information is very detailed, more than 1 sentences, grade it 5.
                                               Output with format: Grade: [grade]. Comment: [comment]


Grade this submission:
{input}
""")

grading_prompts_v5 = PromptTemplate.from_template("""
Evaluate the project for {section}. Use the following grading criteria: {criteria}. Assign a grade between 0 and 5. If the submission fails to address the criteria, even partially, assign a 0. If the submission meets the criteria with the necessary information, assign a 3. For a detailed explanation, beyond one sentence, assign a 5. Please provide your evaluation in this format: Grade: [grade]. Comment: [comment]. Now, grade this submission: {input}.
""")

grading_prompts_v6 = PromptTemplate.from_template("""You are assessing the {section} of a project. Base your evaluation on the following criteria: {criteria}. Assign a score between 0 and 5. If the submission doesn't meet the criteria, give it a 0. If it satisfies the criteria, give it a 3. For submissions with more than one sentence of detail, assign a 5. Format your response as follows: Grade: [grade]. Comment: [comment]. Here is the submission to grade: {input}.""")

grading_prompts_v7 = PromptTemplate.from_template("""Grade the following project submission in the {section} category based on these criteria: {criteria}. Your grade should be 0 if the information is missing, 3 if the criteria are met, and 5 for submissions that provide more than one sentence of detailed information. Use this format: Grade: [grade]. Comment: [comment]. Please grade this submission: {input}.""")

grading_prompts_v8 = PromptTemplate.from_template("""Please review the {section} section of this project. Follow these criteria: {criteria}. Assign a grade from 0 to 5. Give a 0 if the submission doesn’t provide the necessary information, a 3 for meeting the requirements, and a 5 for submissions that include detailed, multi-sentence responses. Format your response as follows: Grade: [grade]. Comment: [comment]. Now, assess this submission: {input}.""")

def generate_prompt(rubric: dict, part_name: str):
   if part_name not in rubric:
      return f"No rubric found for {part_name}."

   prompt = """
   You are an evaluator. Below is a rubric for evaluating various parts of a project report. Please evaluate each section based on the specific criteria provided for each section.
   """

   for criterion in rubric[part_name]['criteria']:
      prompt += f"- {criterion['name']} (Score Range: {criterion['grade_range']})\n"

   prompt += f"""
   Instructions:
   1. Assign a score based on the criteria and provided grade range.
   2. For **each score assigned**, provide a **clear and detailed explanation** that justifies the score, including references to specific aspects of the project report that led to the score.
      - If the score is low, explain what was missing or insufficient.
      - If the score is high, explain what was well-done or exceeded expectations.
      - Focus only on the evaluation of '{part_name}' as a whole.
      - Do not create or refer to any sub-sections under '{part_name}'.
   3. Ensure that **every question** under '{part_name}' is evaluated. Do not skip or omit any questions, even if the response is minimal.
   4. The explanation should focus on **how well the report meets the criteria** outlined for that section.
   5. The 'Total Score' should be the sum of all individual question scores, and 'Overall Description' should summarize the evaluation.
   6. Ensure the JSON is well-formed, properly indented, and does not contain any syntax errors.
      - Example format:
         {{
               "{part_name}": {{
                  "Question 1": {{
                     "score": "",
                     "explanation": ""
                  }},
                  "Question 2": {{
                     "score": "",
                     "explanation": ""
                  }},
                  ...
                  "Total Score": "",
                  "Overall Description": ""
               }}
         }}
   7. Respond only with the JSON object. Do not include any explanations outside the JSON.
   """
   return prompt
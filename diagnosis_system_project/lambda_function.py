import json
import boto3
import re

def get_input_as_list(input, list):
    my_list = [0] * 131
    for word in input:
        my_list[list.index(word)] = 1
    my_list = [my_list]
    return my_list
        

def lambda_handler(event, context):

    symptoms = ['itching', ' skin_rash', ' continuous_sneezing', ' shivering',
       ' stomach_pain', ' acidity', ' vomiting', ' indigestion',
       ' muscle_wasting', ' patches_in_throat', ' fatigue', ' weight_loss',
       ' sunken_eyes', ' cough', ' headache', ' chest_pain', ' back_pain',
       ' weakness_in_limbs', ' chills', ' joint_pain', ' yellowish_skin',
       ' constipation', ' pain_during_bowel_movements', ' breathlessness',
       ' cramps', ' weight_gain', ' mood_swings', ' neck_pain',
       ' muscle_weakness', ' stiff_neck', ' pus_filled_pimples',
       ' burning_micturition', ' bladder_discomfort', ' high_fever',
       ' nodal_skin_eruptions', ' ulcers_on_tongue', ' loss_of_appetite',
       ' restlessness', ' dehydration', ' dizziness',
       ' weakness_of_one_body_side', ' lethargy', ' nausea', ' abdominal_pain',
       ' pain_in_anal_region', ' sweating', ' bruising',
       ' cold_hands_and_feets', ' anxiety', ' knee_pain',
       ' swelling_joints', ' blackheads', ' foul_smell_of urine',
       ' skin_peeling', ' blister', ' dischromic _patches',
       ' watering_from_eyes', ' extra_marital_contacts', ' diarrhoea',
       ' loss_of_balance', ' blurred_and_distorted_vision',
       ' altered_sensorium', ' dark_urine', ' swelling_of_stomach',
       ' bloody_stool', ' obesity', ' hip_joint_pain', ' movement_stiffness',
       ' spinning_movements', ' scurring', ' continuous_feel_of_urine',
       ' silver_like_dusting', ' red_sore_around_nose', ' spotting_ urination',
       ' passage_of_gases', ' irregular_sugar_level', ' family_history',
       ' lack_of_concentration', ' excessive_hunger', ' yellowing_of_eyes',
       ' distention_of_abdomen', ' irritation_in_anus', ' swollen_legs',
       ' painful_walking', ' small_dents_in_nails', ' yellow_crust_ooze',
       ' internal_itching', ' mucoid_sputum',
       ' history_of_alcohol_consumption', ' swollen_blood_vessels',
       ' unsteadiness', ' inflammatory_nails', ' depression',
       ' fluid_overload', ' swelled_lymph_nodes', ' malaise',
       ' prominent_veins_on_calf', ' puffy_face_and_eyes', ' fast_heart_rate',
       ' irritability', ' muscle_pain', ' mild_fever', ' yellow_urine',
       ' phlegm', ' enlarged_thyroid', ' increased_appetite',
       ' visual_disturbances', ' brittle_nails', ' drying_and_tingling_lips',
       ' polyuria', ' pain_behind_the_eyes', ' toxic_look_(typhos)',
       ' throat_irritation', ' swollen_extremeties', ' slurred_speech',
       ' red_spots_over_body', ' belly_pain', ' receiving_blood_transfusion',
       ' acute_liver_failure', ' redness_of_eyes', ' rusty_sputum',
       ' abnormal_menstruation', ' receiving_unsterile_injections', ' coma',
       ' sinus_pressure', ' palpitations', ' stomach_bleeding', ' runny_nose',
       ' congestion', ' blood_in_sputum', ' loss_of_smell']
    
    diseases = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis',
       'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes ',
       'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine',
       'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice',
       'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
       'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
       'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
       'Dimorphic hemmorhoids(piles)', 'Heart attack', 'Varicose veins',
       'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
       'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne',
       'Urinary tract infection', 'Psoriasis', 'Impetigo']

    words = event['body'].split(',')[:-1]
    inputs = get_input_as_list(words, symptoms)
    x = [0] * 131
    #inputs = np.zeros(len(symptoms))
    #inputs[indeces] = 1

    # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
    runtime = boto3.Session().client('sagemaker-runtime')

    # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
    response = runtime.invoke_endpoint(EndpointName = 'sagemaker-scikit-learn-2021-08-22-04-41-55-040',
                                       # The name of the endpoint we created
                                       ContentType = 'text/csv',
                                       Body =(','.join([str(val) for val in inputs)+'\n'+(','.join([str(val) for val in x]))).encode('utf-8')
                                       )

    # The response is an HTTP response whose body contains the result of our inference
    #result = response['Body'].read().decode('utf-8')
    try:
        result = response['Body'].read().encode('utf-8')
        o = re.findall(r'\d+', result)[:41]
        result = diseases[o.index('1')]
    except ValueError:
        result = "sorry we can't identify the disease"

    return {
        'statusCode' : 200,
        'headers' : { 'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*' },
        'body' : str(result)
    }

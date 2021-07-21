covid.far: covid.grm covid_symptoms3.far place_country.far local_address.far activity.far
	thraxcompiler --input_grammar=$< --output_far=$@

covid_symptoms3.far: covid_symptoms3.grm example.far exclamation.far numbers.far new_var_files/covid_symptoms_variables/VAR_DO_HAVE_YOU.far new_var_files/covid_symptoms_variables/VAR_I_HAVE.far new_var_files/covid_symptoms_variables/VAR_WHEN.far new_var_files/covid_symptoms_variables/VAR_WHAT_WHY.far new_var_files/covid_symptoms_variables/VAR_CHORES.far new_var_files/covid_symptoms_variables/VAR_I_THINK.far txt_resource_files/chinesefirstnames.txt txt_resource_files/chineselastnames.txt txt_resource_files/symptom.txt txt_resource_files/people.txt txt_resource_files/timeframe.txt
	thraxcompiler --input_grammar=$< --output_far=$@

example.far: example.grm byte.far numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

byte.far: byte.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

numbers.far: numbers.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

exclamation.far: exclamation.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/covid_symptoms_variables/VAR_DO_HAVE_YOU.far: new_var_files/covid_symptoms_variables/VAR_DO_HAVE_YOU.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/covid_symptoms_variables/VAR_I_HAVE.far: new_var_files/covid_symptoms_variables/VAR_I_HAVE.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/covid_symptoms_variables/VAR_WHEN.far: new_var_files/covid_symptoms_variables/VAR_WHEN.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/covid_symptoms_variables/VAR_WHAT_WHY.far: new_var_files/covid_symptoms_variables/VAR_WHAT_WHY.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/covid_symptoms_variables/VAR_CHORES.far: new_var_files/covid_symptoms_variables/VAR_CHORES.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/covid_symptoms_variables/VAR_I_THINK.far: new_var_files/covid_symptoms_variables/VAR_I_THINK.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

place_country.far: place_country.grm example.far numbers.far new_var_files/place_country_variables/VAR_WHERE_WHICH.far new_var_files/place_country_variables/VAR_I_WENT.far new_var_files/place_country_variables/VAR_I_CAME.far txt_resource_files/businesses_and_places.txt txt_resource_files/dates.txt txt_resource_files/time.txt txt_resource_files/countries.txt txt_resource_files/timeframe.txt
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/place_country_variables/VAR_WHERE_WHICH.far: new_var_files/place_country_variables/VAR_WHERE_WHICH.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/place_country_variables/VAR_I_WENT.far: new_var_files/place_country_variables/VAR_I_WENT.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/place_country_variables/VAR_I_CAME.far: new_var_files/place_country_variables/VAR_I_CAME.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

local_address.far: local_address.grm example.far numbers.far new_var_files/local_addresses_variables/VAR_WHERE_WHICH.far new_var_files/local_addresses_variables/VAR_I_WENT.far txt_resource_files/dates.txt txt_resource_files/time.txt txt_resource_files/timeframe.txt txt_resource_files/roads_and_streets.txt txt_resource_files/venues-filtered.txt txt_resource_files/regions.txt
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/local_addresses_variables/VAR_WHERE_WHICH.far: new_var_files/local_addresses_variables/VAR_WHERE_WHICH.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/local_addresses_variables/VAR_I_WENT.far: new_var_files/local_addresses_variables/VAR_I_WENT.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

activity.far: activity.grm example.far numbers.far new_var_files/activity_variables/VAR_CHORES.far txt_resource_files/chinesefirstnames.txt txt_resource_files/chineselastnames.txt txt_resource_files/people.txt
	thraxcompiler --input_grammar=$< --output_far=$@

new_var_files/activity_variables/VAR_CHORES.far: new_var_files/activity_variables/VAR_CHORES.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

clean:
	rm -f covid_symptoms3.far place_country.far local_address.far activity.far example.far exclamation.far numbers.far new_var_files/covid_symptoms_variables/VAR_DO_HAVE_YOU.far new_var_files/covid_symptoms_variables/VAR_I_HAVE.far new_var_files/covid_symptoms_variables/VAR_WHEN.far new_var_files/covid_symptoms_variables/VAR_WHAT_WHY.far new_var_files/covid_symptoms_variables/VAR_CHORES.far new_var_files/covid_symptoms_variables/VAR_I_THINK.far byte.far new_var_files/place_country_variables/VAR_WHERE_WHICH.far new_var_files/place_country_variables/VAR_I_WENT.far new_var_files/place_country_variables/VAR_I_CAME.far new_var_files/local_addresses_variables/VAR_WHERE_WHICH.far new_var_files/local_addresses_variables/VAR_I_WENT.far new_var_files/activity_variables/VAR_CHORES.far

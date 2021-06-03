test.far: test.grm numbers.far example.far resources/roads_and_streets.txt resources/venues-filtered.txt resources/regions.txt
	thraxcompiler --input_grammar=$< --output_far=$@

numbers.far: numbers.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

byte.far: byte.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

example.far: example.grm byte.far numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

clean:
	rm -f numbers.far example.far byte.far

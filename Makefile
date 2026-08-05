
THRIFT_CONFIG := ci/thrift.env
include $(THRIFT_CONFIG)

.PHONY: check-thrift-config
check-thrift-config:
	@grep -Fq '"thrift >=$(THRIFT_VERSION)"' pyproject.toml || { echo "pyproject.toml Thrift minimum must match $(THRIFT_CONFIG) ($(THRIFT_VERSION))" >&2; exit 1; }
	@grep -Fqx -- '- thrift>=$(THRIFT_VERSION)' environment.yml || { echo "environment.yml Thrift minimum must match $(THRIFT_CONFIG) ($(THRIFT_VERSION))" >&2; exit 1; }

.PHONY: thrift
thrift: check-thrift-config
	@actual_version="$$(thrift -version)"; \
		test "$$actual_version" = "Thrift version $(THRIFT_VERSION)" || { echo "Expected Thrift version $(THRIFT_VERSION), got $$actual_version" >&2; exit 1; }
	rm -rf src/heavydb/thrift/
	mkdir -p src/heavydb/thrift/
	mkdir -p src/heavydb/common/
	mkdir -p src/heavydb/completion_hints/
	mkdir -p src/heavydb/extension_functions/
	mkdir -p src/heavydb/serialized_result_set/
	# The thrift python generator builds __init__.py file(s).
	# If the generator is run in the python source directory
	# which contains __init__.py files, they will be over written,
	# To prevent this the make file uses the gen-py folder and
	# then cp the needed files in the directories that the python
	# source code's imports and package commands expect them in.
	#
	# The copied versions of the files are listed in the
	# .gitignore file in this dir and as generated files 
	# shouldn't be commited.
	# 
	thrift -r -gen py thrift_definition/heavy.thrift
	cp -r gen-py/heavydb/thrift/* src/heavydb/thrift/
	cp -r gen-py/heavydb/common/* src/heavydb/common/
	cp -r gen-py/heavydb/completion_hints/* src/heavydb/completion_hints/
	cp -r gen-py/heavydb/extension_functions/* src/heavydb/extension_functions/
	cp -r gen-py/heavydb/serialized_result_set/* src/heavydb/serialized_result_set/

.PHONY: build
build: thrift
	python -m build

.PHONY: publish
publish: build
	twine upload dist/*

.PHONY: clean
clean:
	rm -rf dist
	rm -rf build
	rm -rf src/*.egg-info
	rm -rf gen-py
	rm -rf src/heavydb/thrift/
	rm -rf src/heavydb/common
	rm -rf src/heavydb/completion_hints
	rm -rf src/heavydb/serialized_result_set
	rm -rf src/heavydb/extension_functions

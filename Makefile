#
#   MIT Licensed
#
#   git@github.com/rstms/tzc
#   mkrueger@rstms.net
#

help:
	@echo Targets:  bump-patch bump-minor bump-major

define bump
bumpversion $1;
dotenv set VERSION $$(cat VERSION);
sed "s/^\(.*__version__.*=.*'\)\(.*\)\('.*\)$$/\1$$(cat VERSION)\3/" -i tzc/__init__.py
endef

bump-patch:
	$(call bump,patch)

bump-minor:
	$(call bump,minor)

bump-major:
	$(call bump,major)

<?xml version="1.0" encoding="UTF-8"?>
<package-plan version="1.0">
  <outcome>
    Create one canonical Python package template, make ontok-core and ontok-ex fully
    ready to publish, and make every deferred ONTOK package as complete as possible
    without inventing its unimplemented semantics.
  </outcome>

  <scope>
    <included>
      <item>The virtual uv workspace and shared development configuration.</item>
      <item>A canonical, non-publishable Python package template.</item>
      <item>Complete distribution metadata for every Python package.</item>
      <item>Complete semantic and package tests for ontok-core and ontok-ex.</item>
      <item>Complete package scaffolding for ontok-vsm, ontok-scim, and ontok-st.</item>
      <item>CI, artifact proof, and a dormant release workflow.</item>
    </included>
    <excluded>
      <item>Publishing any distribution to PyPI or TestPyPI.</item>
      <item>Creating fake implementations for deferred modules.</item>
      <item>Creating tests that merely retest guarantees already owned by Pydantic.</item>
      <item>Copying implementation-independent specifications into Python source trees.</item>
      <item>Publishing the root workspace or the package template.</item>
    </excluded>
  </scope>

  <fixed-decisions>
    <decision id="license">
      <value>Apache-2.0</value>
      <copyright>Copyright 2026 Kyle Tobin</copyright>
      <repository-files>LICENSE and NOTICE</repository-files>
    </decision>
    <decision id="repository">
      <url>https://github.com/kyzobuild/ontok</url>
      <issues>https://github.com/kyzobuild/ontok/issues</issues>
    </decision>
    <decision id="workspace">
      <value>The root pyproject.toml remains the non-publishable virtual uv workspace.</value>
      <rule>Every distributable remains an independent workspace member with its own pyproject.toml.</rule>
    </decision>
    <decision id="namespace">
      <value>ontok is one implicit PEP 420 namespace shared by independent distributions.</value>
      <rule>No ontok/__init__.py may exist in any distribution.</rule>
      <rule>Every typed subpackage contains its own py.typed marker.</rule>
    </decision>
    <decision id="python">
      <minimum>3.13</minimum>
      <tested>3.13 and 3.14</tested>
    </decision>
    <decision id="build-backend">
      <requirement>uv_build&gt;=0.12.12,&lt;0.13</requirement>
    </decision>
    <decision id="pydantic">
      <core-requirement>pydantic&gt;=2.9,&lt;3</core-requirement>
    </decision>
    <decision id="versions">
      <release-candidates version="0.1.0">ontok-core ontok-ex</release-candidates>
      <deferred version="0.0.0">ontok-vsm ontok-scim ontok-st</deferred>
      <initial-release-tag>v0.1.0</initial-release-tag>
    </decision>
    <decision id="publication">
      <release-candidates>ontok-core then ontok-ex</release-candidates>
      <withheld>ontok-vsm ontok-scim ontok-st ontok-workspace ontok-module-template</withheld>
    </decision>
    <decision id="specifications">
      <value>spec/ remains the single source of implementation-independent semantics.</value>
      <rule>Package documentation links to the canonical specification on GitHub.</rule>
    </decision>
    <decision id="template">
      <path>templates/python/ontok-module</path>
      <rule>The template lives outside packages/python and is never a workspace member.</rule>
      <rule>The template uses explicit replacement tokens and is never itself published.</rule>
    </decision>
  </fixed-decisions>

  <package-contract>
    <required-files>
      <file>pyproject.toml</file>
      <file>README.md</file>
      <file>LICENSE</file>
      <file>NOTICE</file>
      <file>src/ontok/{module}/__init__.py</file>
      <file>src/ontok/{module}/py.typed</file>
    </required-files>
    <required-project-metadata>
      <field>name</field>
      <field>version</field>
      <field>description</field>
      <field>readme</field>
      <field>requires-python</field>
      <field>license</field>
      <field>license-files</field>
      <field>authors</field>
      <field>keywords</field>
      <field>classifiers</field>
      <field>dependencies</field>
      <field>urls</field>
      <field>import-names</field>
      <field>import-namespaces</field>
    </required-project-metadata>
    <metadata-values>
      <license>Apache-2.0</license>
      <license-files>LICENSE and NOTICE</license-files>
      <author name="Kyle Tobin" email="tobin.kyle@gmail.com"/>
      <homepage>https://github.com/kyzobuild/ontok</homepage>
      <repository>https://github.com/kyzobuild/ontok</repository>
      <issues>https://github.com/kyzobuild/ontok/issues</issues>
      <classifiers>
        <classifier>Programming Language :: Python :: 3</classifier>
        <classifier>Programming Language :: Python :: 3.13</classifier>
        <classifier>Programming Language :: Python :: 3.14</classifier>
        <classifier>Typing :: Typed</classifier>
        <classifier>Intended Audience :: Developers</classifier>
        <classifier>Topic :: Software Development :: Libraries</classifier>
      </classifiers>
      <rule>Use the SPDX license expression; do not add a deprecated License classifier.</rule>
      <rule>Each distribution declares ontok as its shared import namespace.</rule>
      <rule>Each distribution declares its own dotted subpackage as its provided import name.</rule>
    </metadata-values>
    <build-values>
      <backend>uv_build</backend>
      <backend-requirement>uv_build&gt;=0.12.12,&lt;0.13</backend-requirement>
      <module-name>ontok.{module}</module-name>
      <source-distribution>Include tests, README, LICENSE, NOTICE, pyproject.toml, and source.</source-distribution>
      <wheel>Include source, py.typed, LICENSE, NOTICE, and distribution metadata; exclude tests.</wheel>
    </build-values>
    <dependency-rules>
      <rule>ontok-core depends on Pydantic and no ONTOK distribution.</rule>
      <rule>Each extension declares ontok-core&gt;=0.1.0,&lt;0.2.0.</rule>
      <rule>tool.uv.sources may bind ontok-core to the workspace for development.</rule>
      <rule>No workspace path or editable dependency may appear in published metadata.</rule>
    </dependency-rules>
    <documentation-rules>
      <rule>Every package README states installation, Python support, responsibility, namespace, and status.</rule>
      <rule>Implemented packages include one minimal public-API example.</rule>
      <rule>Deferred packages explicitly state that they are not release candidates.</rule>
      <rule>Specification links are absolute canonical GitHub links.</rule>
    </documentation-rules>
  </package-contract>

  <execution-policy>
    <rule>Execute tasks in sequence order.</rule>
    <rule>Begin a task only after every depends-on task is complete.</rule>
    <rule>Run the task validation before proceeding.</rule>
    <rule>Fix the modeled cause of every failure; never suppress a gate.</rule>
    <rule>Make no semantic changes outside the task that owns them.</rule>
    <rule>Do not publish from this plan.</rule>
  </execution-policy>

  <tasks>
    <task id="P00" sequence="00" status="complete">
      <name>Establish legal and repository identity</name>
      <outputs>
        <output>LICENSE contains the Apache License 2.0 text.</output>
        <output>NOTICE identifies Kyle Tobin as the 2026 copyright holder.</output>
        <output>README.md links to LICENSE.</output>
        <output>origin is https://github.com/kyzobuild/ontok.git.</output>
      </outputs>
      <validation>
        <command><![CDATA[git remote get-url origin]]></command>
        <command><![CDATA[git diff --check]]></command>
      </validation>
    </task>

    <task id="P01" sequence="01" status="complete" depends-on="P00">
      <name>Normalize the virtual workspace and quality gates</name>
      <actions>
        <action>Keep the root pyproject.toml and tool.uv.package=false.</action>
        <action>Keep packages/python/* as the workspace-member boundary.</action>
        <action>Keep the shared uv.lock at repository root.</action>
        <action>Add pytest strict_config, strict_markers, and strict xfail behavior.</action>
        <action>Make CI commands explicit: pytest, Ruff lint, Ruff format, basedpyright, and import-linter.</action>
        <action>Add artifact-checking development tools only when a later task uses them.</action>
        <action>Update uv.lock after all declared dependency changes in this task.</action>
      </actions>
      <validation>
        <command><![CDATA[uv lock --check]]></command>
        <command><![CDATA[uv run pytest -q]]></command>
        <command><![CDATA[uv run ruff check .]]></command>
        <command><![CDATA[uv run ruff format --check .]]></command>
        <command><![CDATA[uv run basedpyright]]></command>
        <command><![CDATA[uv run lint-imports --no-cache]]></command>
      </validation>
      <done>
        The root is unambiguously non-publishable and every repository quality gate has one
        canonical command that passes locally.
      </done>
    </task>

    <task id="P02" sequence="02" status="pending" depends-on="P01">
      <name>Create the canonical package template</name>
      <actions>
        <action>Create templates/python/ontok-module outside workspace membership.</action>
        <action>Create tokenized pyproject.toml, README.md, source tree, py.typed, tests tree, LICENSE, and NOTICE.</action>
        <action>Represent distribution name, module name, description, status, keywords, dependencies, and specification URL with explicit replacement tokens.</action>
        <action>Include the complete package contract from this plan in the template README.</action>
        <action>Include workspace-dependency instructions without hard-coding a false dependency.</action>
        <action>Include a creation checklist requiring specification, realization, semantic test, artifact test, and workspace registration.</action>
        <action>Add a deterministic template rendering check using a temporary directory.</action>
        <action>Prove the rendered package metadata and PEP 420 layout without adding it to the workspace.</action>
      </actions>
      <validation>
        <command><![CDATA[uv run pytest -q tests/package_template]]></command>
        <command><![CDATA[git diff --check]]></command>
      </validation>
      <done>
        A new ONTOK module can be created by replacing named tokens, and a rendered copy
        constructs valid metadata and the exact required filesystem shape.
      </done>
    </task>

    <task id="P03" sequence="03" status="pending" depends-on="P02">
      <name>Normalize ontok-core as a release candidate</name>
      <actions>
        <action>Apply the complete package contract to packages/python/ontok-core.</action>
        <action>Set build-system requirement to uv_build&gt;=0.12.12,&lt;0.13.</action>
        <action>Set the runtime dependency to pydantic&gt;=2.9,&lt;3.</action>
        <action>Declare Apache-2.0 and package-local LICENSE and NOTICE files.</action>
        <action>Declare ontok as the shared namespace and ontok.core as the provided import.</action>
        <action>Add source-include for tests so tests enter the sdist but not the wheel.</action>
        <action>Keep version 0.1.0 and classify the distribution as Alpha and Typed.</action>
        <action>Do not add __version__; distribution metadata is the version authority.</action>
      </actions>
      <validation>
        <command><![CDATA[uv lock]]></command>
        <command><![CDATA[uv run ruff check packages/python/ontok-core]]></command>
        <command><![CDATA[uv run basedpyright packages/python/ontok-core]]></command>
      </validation>
      <done>
        ontok-core has complete, standards-current, internally consistent distribution
        metadata with no undeclared or unbounded dependency.
      </done>
    </task>

    <task id="P04" sequence="04" status="pending" depends-on="P03">
      <name>Prove the complete Core semantic surface</name>
      <actions>
        <action>Create packages/python/ontok-core/tests.</action>
        <action>Create one real semantic construction that uses every Core primitive and Work together.</action>
        <action>Use only the public ontok.core import surface.</action>
        <action>Prove that the terminal constructed organizational fact preserves the entire primitive graph.</action>
        <action>Do not create field-by-field tests of Pydantic freezing, extras, patterns, awareness, or numeric constraints.</action>
        <action>Do not add mocks, a registry, procedural orchestration, or a second semantic model.</action>
      </actions>
      <validation>
        <command><![CDATA[uv run pytest -q packages/python/ontok-core/tests]]></command>
        <command><![CDATA[uv run ruff check packages/python/ontok-core/tests]]></command>
        <command><![CDATA[uv run basedpyright packages/python/ontok-core/tests]]></command>
      </validation>
      <done>
        One executable organizational construction proves that Core's complete public
        vocabulary composes as one kernel; no test merely restates substrate guarantees.
      </done>
    </task>

    <task id="P05" sequence="05" status="pending" depends-on="P04">
      <name>Normalize ontok-ex as a release candidate</name>
      <actions>
        <action>Apply the complete package contract to packages/python/ontok-ex.</action>
        <action>Set build-system requirement to uv_build&gt;=0.12.12,&lt;0.13.</action>
        <action>Keep ontok-core&gt;=0.1.0,&lt;0.2.0 as the published dependency.</action>
        <action>Keep tool.uv.sources ontok-core workspace=true for local development.</action>
        <action>Declare Apache-2.0 and package-local LICENSE and NOTICE files.</action>
        <action>Declare ontok as the shared namespace and ontok.ex as the provided import.</action>
        <action>Add source-include for tests so tests enter the sdist but not the wheel.</action>
        <action>Keep version 0.1.0 and classify the distribution as Alpha and Typed.</action>
        <action>Export every execution-state type required by the public arrival API.</action>
        <action>Make every EX test import only from ontok.ex and ontok.core public surfaces.</action>
      </actions>
      <validation>
        <command><![CDATA[uv lock]]></command>
        <command><![CDATA[uv run pytest -q packages/python/ontok-ex/tests]]></command>
        <command><![CDATA[uv run ruff check packages/python/ontok-ex]]></command>
        <command><![CDATA[uv run basedpyright packages/python/ontok-ex]]></command>
      </validation>
      <done>
        ontok-ex exposes one coherent public execution API, its tests consume no private
        implementation path, and its distribution metadata is release-complete.
      </done>
    </task>

    <task id="P06" sequence="06" status="pending" depends-on="P05">
      <name>Confirm EX's production execution patterns</name>
      <actions>
        <action>Retain one test file for sequence.</action>
        <action>Retain one test file for fan-out.</action>
        <action>Retain one test file for join.</action>
        <action>Retain one test file for either-order blocked and resumed execution.</action>
        <action>Retain one test file for terminal execution.</action>
        <action>Ensure tests supply request and Completion events as transport facts.</action>
        <action>Ensure production source owns Program declarations and execution construction.</action>
        <action>Ensure no test revalidates a Pydantic guarantee or implements a shadow executor.</action>
      </actions>
      <validation>
        <command><![CDATA[uv run pytest -q packages/python/ontok-ex/tests]]></command>
        <command><![CDATA[uv run ruff check packages/python/ontok-ex/tests]]></command>
        <command><![CDATA[uv run basedpyright packages/python/ontok-ex/tests]]></command>
      </validation>
      <done>
        The five tests are realistic transport-independent executions over production EX
        constructs and collectively reach terminal completion.
      </done>
    </task>

    <task id="P07" sequence="07" status="pending" depends-on="P06">
      <name>Complete deferred-package scaffolding without fake semantics</name>
      <packages>
        <package distribution="ontok-vsm" module="ontok.vsm" specification="spec/ontok-vsm.xml"/>
        <package distribution="ontok-scim" module="ontok.scim" specification="spec/ontok-scim.xml"/>
        <package distribution="ontok-st" module="ontok.st" specification="spec/ontok-st.xml"/>
      </packages>
      <actions>
        <action>Apply the canonical package template to each deferred package.</action>
        <action>Set each deferred package version to 0.0.0.</action>
        <action>Classify each deferred package as Planning and Typed.</action>
        <action>Add package-local LICENSE, NOTICE, and py.typed.</action>
        <action>Keep the exact ontok-core&gt;=0.1.0,&lt;0.2.0 dependency and workspace source.</action>
        <action>Use absolute canonical links to each module specification.</action>
        <action>State explicitly that the package is withheld from publication.</action>
        <action>Keep __init__.py empty until real public semantics exist.</action>
        <action>Add no semantic tests and no placeholder domain types.</action>
        <action>Update uv.lock to the 0.0.0 scaffold versions.</action>
      </actions>
      <validation>
        <command><![CDATA[uv lock --check]]></command>
        <command><![CDATA[uv run python -c "import ontok.vsm, ontok.scim, ontok.st"]]></command>
        <command><![CDATA[uv run ruff check packages/python/ontok-vsm packages/python/ontok-scim packages/python/ontok-st]]></command>
        <command><![CDATA[uv run basedpyright packages/python/ontok-vsm packages/python/ontok-scim packages/python/ontok-st]]></command>
      </validation>
      <done>
        Every deferred package is structurally complete, visibly unreleased, typed, licensed,
        documented, and ready to receive semantics without publishing an empty 0.1.0.
      </done>
    </task>

    <task id="P08" sequence="08" status="pending" depends-on="P07">
      <name>Make repository and package documentation release-accurate</name>
      <actions>
        <action>Add ontok-ex to every root package list and workspace tree.</action>
        <action>Reconcile the root execution discussion with the existence and responsibility of ontok-ex.</action>
        <action>Add installation commands for ontok-core and ontok-ex.</action>
        <action>Add one minimal public-API example to the Core and EX package READMEs.</action>
        <action>Add Python support, license, source, issues, status, and specification links to every package README.</action>
        <action>Replace every unavailable relative specification reference with its canonical GitHub URL.</action>
        <action>Keep deferred package documentation explicit about absent implementation.</action>
      </actions>
      <validation>
        <command><![CDATA[git grep -n "spec/ontok-" -- "packages/python/*/README.md"]]></command>
        <command><![CDATA[git grep -n "ontok-ex" README.md]]></command>
        <command><![CDATA[git diff --check]]></command>
      </validation>
      <done>
        Repository and PyPI-facing documentation describe the packages that actually exist,
        expose usable installation paths, and contain no broken repository-relative claims.
      </done>
    </task>

    <task id="P09" sequence="09" status="pending" depends-on="P08">
      <name>Add continuous integration</name>
      <actions>
        <action>Create .github/workflows/ci.yml.</action>
        <action>Trigger on pull requests and pushes to main.</action>
        <action>Run locked dependency installation.</action>
        <action>Run the complete quality gate on Python 3.13 and 3.14.</action>
        <action>Run Core against the declared minimum Pydantic 2.9 line in an isolated Python 3.13 environment.</action>
        <action>Run import-linter without a writable cache requirement.</action>
        <action>Build artifacts only after source gates pass.</action>
        <action>Pin third-party GitHub Actions to immutable commit SHAs with version comments.</action>
        <action>Grant no write or OIDC permission to CI jobs.</action>
      </actions>
      <validation>
        <command><![CDATA[uv run pytest -q]]></command>
        <command><![CDATA[uv run ruff check .]]></command>
        <command><![CDATA[uv run ruff format --check .]]></command>
        <command><![CDATA[uv run basedpyright]]></command>
        <command><![CDATA[uv run lint-imports --no-cache]]></command>
      </validation>
      <done>
        Every supported interpreter and declared minimum dependency is continuously proven,
        and no publication credential exists in the CI execution graph.
      </done>
    </task>

    <task id="P10" sequence="10" status="pending" depends-on="P09">
      <name>Prove wheel and source-distribution artifacts</name>
      <actions>
        <action>Build ontok-core wheel and sdist with workspace sources disabled.</action>
        <action>Build ontok-ex wheel and sdist with workspace sources disabled.</action>
        <action>Build each deferred scaffold to prove packaging completeness, but mark all outputs non-release.</action>
        <action>Build a wheel from each sdist to prove source-distribution completeness.</action>
        <action>Run standards metadata checks over every artifact.</action>
        <action>Inspect every wheel and sdist file list against the package contract.</action>
        <action>Prove tests are present in sdists and absent from wheels.</action>
        <action>Prove LICENSE, NOTICE, README, py.typed, and the exact module are present.</action>
        <action>Prove no editable path, workspace path, test cache, build cache, or foreign ONTOK module is present.</action>
        <action>Install Core and EX wheels together into a fresh isolated environment without editable sources.</action>
        <action>Import ontok.core and ontok.ex together and run the Core and EX semantic suites against installed artifacts.</action>
        <action>Record artifact names and SHA-256 digests as CI outputs.</action>
      </actions>
      <validation>
        <command><![CDATA[uv build --package ontok-core --no-sources]]></command>
        <command><![CDATA[uv build --package ontok-ex --no-sources]]></command>
        <command><![CDATA[uv publish --dry-run dist/*]]></command>
      </validation>
      <done>
        The exact files intended for PyPI, rather than editable workspace sources, install
        together and execute the complete semantic proof with correct metadata and contents.
      </done>
    </task>

    <task id="P11" sequence="11" status="pending" depends-on="P10">
      <name>Create the dormant trusted-publishing workflow</name>
      <actions>
        <action>Create .github/workflows/release.yml.</action>
        <action>Trigger only from a published GitHub release whose tag matches v{version}.</action>
        <action>Require package metadata versions to equal the release tag.</action>
        <action>Build once in an unprivileged job and consume only its tested artifacts.</action>
        <action>Publish ontok-core in a protected pypi environment.</action>
        <action>Publish ontok-ex only after successful Core publication.</action>
        <action>Grant id-token: write only to the two publication jobs.</action>
        <action>Use PyPI Trusted Publishing and default provenance attestations.</action>
        <action>Reference only ontok-core and ontok-ex by exact artifact paths.</action>
        <action>Exclude root, template, VSM, SCIM, and ST by construction rather than filtering a wildcard.</action>
        <action>Pin third-party GitHub Actions to immutable commit SHAs with version comments.</action>
        <action>Document the future external step: register this workflow and pypi environment as pending publishers for ontok-core and ontok-ex.</action>
        <action>Do not create a GitHub release, tag v0.1.0, register a publisher, or upload an artifact during this plan.</action>
      </actions>
      <validation>
        <command><![CDATA[Confirm workflow package paths resolve only to Core and EX artifacts.]]></command>
        <command><![CDATA[Confirm only publication jobs declare id-token: write.]]></command>
        <command><![CDATA[Confirm CI and build jobs remain read-only.]]></command>
      </validation>
      <done>
        Publication requires one deliberate future GitHub release and protected-environment
        approval; no present repository action can accidentally publish a deferred package.
      </done>
    </task>

    <task id="P12" sequence="12" status="pending" depends-on="P11">
      <name>Run the terminal package-readiness proof</name>
      <actions>
        <action>Start from a clean checkout at one commit.</action>
        <action>Run the locked source quality gate.</action>
        <action>Run template rendering proof.</action>
        <action>Run Core's complete semantic construction.</action>
        <action>Run EX's five production execution patterns.</action>
        <action>Run the complete artifact proof.</action>
        <action>Verify package versions and dependency ranges against the release graph.</action>
        <action>Verify all five normalized PyPI project names remain available.</action>
        <action>Verify root and template cannot enter release artifacts.</action>
        <action>Verify the working tree is clean.</action>
        <action>Write no exception list; every failed fact returns ownership to the task that defines it.</action>
      </actions>
      <validation>
        <command><![CDATA[uv lock --check]]></command>
        <command><![CDATA[uv run pytest -q]]></command>
        <command><![CDATA[uv run ruff check .]]></command>
        <command><![CDATA[uv run ruff format --check .]]></command>
        <command><![CDATA[uv run basedpyright]]></command>
        <command><![CDATA[uv run lint-imports --no-cache]]></command>
        <command><![CDATA[git diff --check]]></command>
        <command><![CDATA[git status --short]]></command>
      </validation>
      <done>
        ontok-core and ontok-ex are fully ready for a deliberate PyPI release; the template
        is the canonical source for future package scaffolding; VSM, SCIM, and ST are maximally
        complete without invented semantics; all release automation exists but nothing has
        been published.
      </done>
    </task>
  </tasks>

  <terminal-definition-of-done>
    <fact>PACKAGE-PLAN.md is valid XML and every task P00 through P12 is complete.</fact>
    <fact>The repository root remains a virtual, non-distributable uv workspace.</fact>
    <fact>The canonical package template renders and validates outside workspace membership.</fact>
    <fact>Core's one semantic test constructs the complete kernel rather than substrate trivia.</fact>
    <fact>EX's five tests execute sequence, fan-out, join, blocked/resumed, and terminal patterns.</fact>
    <fact>Core and EX wheels and sdists install and execute from a clean environment.</fact>
    <fact>Core and EX metadata is complete, typed, licensed, linked, bounded, and standards-current.</fact>
    <fact>VSM, SCIM, and ST are complete typed scaffolds at version 0.0.0 and cannot be published by the release workflow.</fact>
    <fact>CI proves source, type, architecture, formatting, dependency, template, and artifact facts.</fact>
    <fact>The release workflow uses protected OIDC publication in Core-then-EX order.</fact>
    <fact>No PyPI or TestPyPI upload has occurred.</fact>
  </terminal-definition-of-done>
</package-plan>

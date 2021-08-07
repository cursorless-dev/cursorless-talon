import * as vscode from "vscode";
import { addDecorationsToEditors } from "./addDecorationsToEditor";
import { DEBOUNCE_DELAY } from "./constants";
import Decorations from "./Decorations";
import graphConstructors from "./graphConstructors";
import { inferFullTargets } from "./inferFullTargets";
import processTargets from "./processTargets";
import FontMeasurements from "./FontMeasurements";
import { ActionType, PartialTarget, ProcessedTargetsContext } from "./Types";
import makeGraph from "./makeGraph";
import { logBranchTypes } from "./debug";
import { TestCase } from "./TestCase";
import { ThatMark } from "./ThatMark";
import { Clipboard } from "./Clipboard";
import { TestCaseRecorder } from "./TestCaseRecorder";

export async function activate(context: vscode.ExtensionContext) {
  const fontMeasurements = new FontMeasurements(context);
  await fontMeasurements.calculate();
  const decorations = new Decorations(fontMeasurements);

  const parseTreeExtension = vscode.extensions.getExtension("pokey.parse-tree");

  if (parseTreeExtension == null) {
    throw new Error("Depends on pokey.parse-tree extension");
  }

  const { getNodeAtLocation: getNodeAtLocationImpl } =
    await parseTreeExtension.activate();

  const getNodeAtLocation = (location: vscode.Location) => {
    try {
      return getNodeAtLocationImpl(location);
    } catch (error) {
      const document = vscode.window.activeTextEditor?.document;
      if (document?.uri === location.uri) {
        throw Error(`Language '${document.languageId}' is not implemented yet`);
      }
      throw error;
    }
  };

  var isActive = vscode.workspace
    .getConfiguration("cursorless")
    .get<boolean>("showOnStart")!;

  function clearEditorDecorations(editor: vscode.TextEditor) {
    decorations.decorations.forEach(({ decoration }) => {
      editor.setDecorations(decoration, []);
    });
  }

  function addDecorations() {
    if (isActive) {
      addDecorationsToEditors(graph.navigationMap, decorations);
    } else {
      vscode.window.visibleTextEditors.forEach(clearEditorDecorations);
      graph.navigationMap.clear();
    }
  }

  var timeoutHandle: NodeJS.Timeout | null = null;

  function addDecorationsDebounced() {
    if (timeoutHandle != null) {
      clearTimeout(timeoutHandle);
    }

    timeoutHandle = setTimeout(() => {
      addDecorations();

      timeoutHandle = null;
    }, DEBOUNCE_DELAY);
  }

  const toggleDecorationsDisposable = vscode.commands.registerCommand(
    "cursorless.toggleDecorations",
    () => {
      isActive = !isActive;
      addDecorationsDebounced();
    }
  );

  const recomputeDecorationStylesDisposable = vscode.commands.registerCommand(
    "cursorless.recomputeDecorationStyles",
    () => {
      fontMeasurements.clearCache();
      recomputeDecorationStyles();
    }
  );

  const graph = makeGraph(graphConstructors);
  const thatMark = new ThatMark();
  const sourceMark = new ThatMark();
  const testCaseRecorder = new TestCaseRecorder(context);

  const cursorlessRecordTestCaseDisposable = vscode.commands.registerCommand(
    "cursorless.recordTestCase",
    async () => {
      if (testCaseRecorder.active) {
        vscode.window.showInformationMessage("Stopped recording test cases");
        testCaseRecorder.stop();
      } else {
        if (await testCaseRecorder.start()) {
          vscode.window.showInformationMessage(
            "Recording test cases for following commands"
          );
        }
      }
    }
  );

  const cursorlessCommandDisposable = vscode.commands.registerCommand(
    "cursorless.command",
    async (
      spokenForm: string,
      actionName: ActionType,
      partialTargets: PartialTarget[],
      ...extraArgs: any[]
    ) => {
      try {
        console.debug(`spokenForm: ${spokenForm}`);
        console.debug(`action: ${actionName}`);
        console.debug(`partialTargets:`);
        console.debug(JSON.stringify(partialTargets, null, 3));
        console.debug(`extraArgs:`);
        console.debug(JSON.stringify(extraArgs, null, 3));

        const action = graph.actions[actionName];

        const selectionContents =
          vscode.window.activeTextEditor?.selections.map((selection) =>
            vscode.window.activeTextEditor!.document.getText(selection)
          ) ?? [];

        const isPaste = actionName === "paste";

        const clipboardContents = isPaste
          ? await Clipboard.readText()
          : undefined;

        const inferenceContext = {
          selectionContents,
          isPaste,
          clipboardContents,
        };

        const targets = inferFullTargets(
          inferenceContext,
          partialTargets,
          action.targetPreferences
        );

        const processedTargetsContext: ProcessedTargetsContext = {
          currentSelections:
            vscode.window.activeTextEditor?.selections.map((selection) => ({
              selection,
              editor: vscode.window.activeTextEditor!,
            })) ?? [],
          currentEditor: vscode.window.activeTextEditor,
          navigationMap: graph.navigationMap,
          thatMark: thatMark.exists() ? thatMark.get() : [],
          sourceMark: sourceMark.exists() ? sourceMark.get() : [],
          getNodeAtLocation,
        };

        const selections = processTargets(processedTargetsContext, targets);

        let testCase: TestCase | null = null;
        if (testCaseRecorder.active) {
          const command = { actionName, partialTargets, extraArgs };
          const context = {
            targets,
            thatMark,
            sourceMark,
            navigationMap: graph.navigationMap!,
            spokenForm,
          };
          testCase = new TestCase(command, context);
          await testCase.recordInitialState();
        }

        const {
          returnValue,
          thatMark: newThatMark,
          sourceMark: newSourceMark,
        } = await action.run(selections, ...extraArgs);

        thatMark.set(newThatMark);
        sourceMark.set(newSourceMark);

        if (testCase != null) {
          await testCase.recordFinalState(returnValue);
          await testCaseRecorder.finish(testCase);
        }

        return returnValue;

        // writeFileSync(
        //   "/Users/pokey/src/cursorless-vscode/inferFullTargetsTests.jsonl",
        //   JSON.stringify({
        //     input: { context, partialTargets, preferredPositions },
        //     expectedOutput: targets,
        //   }) + "\n",
        //   { flag: "a" }
        // );

        // writeFileSync(
        //   "/Users/pokey/src/cursorless-vscode/processTargetsTests.jsonl",
        //   JSON.stringify({
        //     input: {
        //       context: processedTargetsContext,
        //       targets,
        //     },
        //     expectedOutput: selections,
        //   }) + "\n",
        //   { flag: "a" }
        // );

        // const processedTargets = processTargets(navigationMap!, targets);
      } catch (e) {
        vscode.window.showErrorMessage(e.message);
        console.trace(e.message);
        throw e;
      }
    }
  );

  addDecorationsDebounced();

  function checkForEditsOutsideViewport(event: vscode.TextDocumentChangeEvent) {
    const editor = vscode.window.activeTextEditor;
    if (editor == null || editor.document !== event.document) {
      return;
    }
    const { start, end } = editor.visibleRanges[0];
    const ranges = [];
    for (const edit of event.contentChanges) {
      if (
        edit.range.end.isBeforeOrEqual(start) ||
        edit.range.start.isAfterOrEqual(end)
      ) {
        ranges.push(edit.range);
      }
    }
    if (ranges.length > 0) {
      ranges.sort((a, b) => a.start.line - b.start.line);
      const linesText = ranges
        .map((range) => `${range.start.line + 1}-${range.end.line + 1}`)
        .join(", ");
      vscode.window.showWarningMessage(
        `Modification outside of viewport at lines: ${linesText}`
      );
    }
  }

  function handleEdit(edit: vscode.TextDocumentChangeEvent) {
    graph.navigationMap.updateTokenRanges(edit);

    addDecorationsDebounced();

    // TODO. Disabled for now because it triggers on undo as well
    //  wait until next release when there is a cause field
    // checkForEditsOutsideViewport(edit);
  }

  const recomputeDecorationStyles = async () => {
    decorations.destroyDecorations();
    await fontMeasurements.calculate();
    decorations.constructDecorations(fontMeasurements);
    addDecorations();
  };

  context.subscriptions.push(
    cursorlessCommandDisposable,
    cursorlessRecordTestCaseDisposable,
    toggleDecorationsDisposable,
    recomputeDecorationStylesDisposable,
    vscode.workspace.onDidChangeConfiguration(recomputeDecorationStyles),
    vscode.window.onDidChangeTextEditorVisibleRanges(addDecorationsDebounced),
    vscode.window.onDidChangeActiveTextEditor(addDecorationsDebounced),
    vscode.window.onDidChangeVisibleTextEditors(addDecorationsDebounced),
    vscode.window.onDidChangeTextEditorSelection(addDecorationsDebounced),
    vscode.window.onDidChangeTextEditorSelection(
      logBranchTypes(getNodeAtLocation)
    ),
    vscode.workspace.onDidChangeTextDocument(handleEdit),
    {
      dispose() {
        if (timeoutHandle != null) {
          clearTimeout(timeoutHandle);
        }
      },
    }
  );

  return {
    navigationMap: graph.navigationMap,
    thatMark,
    sourceMark,
    addDecorations,
  };
}

// this method is called when your extension is deactivated
export function deactivate() {}
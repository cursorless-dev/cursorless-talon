import {
  createPatternMatchers,
  argumentMatcher,
  leadingMatcher,
  conditionMatcher,
  trailingMatcher,
} from "../util/nodeMatchers";
import {
  NodeMatcherAlternative,
  ScopeType,
  SelectionWithEditor,
} from "../typings/Types";
import { getNodeRange } from "../util/nodeSelectors";
import { SyntaxNode } from "web-tree-sitter";

// Generated by the following command:
// > curl https://raw.githubusercontent.com/tree-sitter/tree-sitter-java/master/src/node-types.json | jq '[.[] | select(.type == "statement" or .type == "declaration") | .subtypes[].type]'
const STATEMENT_TYPES = [
  "annotation_type_declaration",
  "class_declaration",
  "enum_declaration",
  "import_declaration",
  "interface_declaration",
  "module_declaration",
  "package_declaration",
  //   ";",
  "assert_statement",
  "block",
  "break_statement",
  "continue_statement",
  "declaration",
  "do_statement",
  "enhanced_for_statement",
  "expression_statement",
  "for_statement",
  "if_statement",
  "labeled_statement",
  "local_variable_declaration",
  "return_statement",
  "switch_expression",
  "synchronized_statement",
  "throw_statement",
  "try_statement",
  "try_with_resources_statement",
  "while_statement",
  "yield_statement",
];

const nodeMatchers: Partial<Record<ScopeType, NodeMatcherAlternative>> = {
  statement: STATEMENT_TYPES,
  class: "class_declaration",
  className: "class_declaration[name]",
  ifStatement: "if_statement",
  string: "string_literal",
  comment: "comment",
  anonymousFunction: "lambda_expression",
  list: "array_initializer",
  functionCall: "method_invocation",
  map: "block",
  name: ["*[declarator][name]", "*[name]", "formal_parameter.identifier!"],
  namedFunction: ["method_declaration", "constructor_declaration"],
  type: trailingMatcher([
    "generic_type.type_arguments.type_identifier",
    "generic_type.type_identifier",
    "type_identifier",
    "local_variable_declaration[type]",
    "array_creation_expression[type]",
    "formal_parameter[type]",
    "method_declaration[type]",
  ]),
  functionName: [
    "method_declaration.identifier!",
    "constructor_declaration.identifier!",
  ],
  value: leadingMatcher(["*[declarator][value]", "*[value]"], ["="]),
  condition: conditionMatcher("*[condition]"),
  collectionItem: argumentMatcher("array_initializer"),
  argumentOrParameter: argumentMatcher("formal_parameters", "argument_list"),
};

export const patternMatchers = createPatternMatchers(nodeMatchers);

/**
 * Extracts string text fragments in java.
 *
 * This is a hack to deal with the fact that java doesn't have
 * quotation mark tokens as children of the string. Rather than letting
 * the parse tree handle the quotation marks in java, we instead just
 * let the textual surround handle them by letting it see the quotation
 * marks. In other languages we prefer to let the parser handle the
 * quotation marks in case they are more than one character long.
 * @param node The node which might be a string node
 * @param selection The selection from which to expand
 * @returns The range of the string text or null if the node is not a string
 */
export function stringTextFragmentExtractor(
  node: SyntaxNode,
  selection: SelectionWithEditor
) {
  if (node.type === "string_literal") {
    return getNodeRange(node);
  }

  return null;
}
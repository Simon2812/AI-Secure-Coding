import type { Node } from "web-tree-sitter";

export class TaintTracker {
  private tainted = new Set<string>();

  add(varName: string): void {
    this.tainted.add(varName);
  }

  has(varName: string): boolean {
    return this.tainted.has(varName);
  }

  expressionIsTainted(node: Node): boolean {
    return this.nodeContainsTaintedIdentifier(node);
  }

  private nodeContainsTaintedIdentifier(node: Node): boolean {
    if (node.type === "identifier" && this.tainted.has(node.text)) {
      return true;
    }
    for (const child of node.children) {
      if (this.nodeContainsTaintedIdentifier(child)) return true;
    }
    return false;
  }

  propagateAssignments(root: Node, isSourceExpr: (node: Node) => boolean): void {
    let changed = true;
    while (changed) {
      changed = false;
      for (const node of walkAll(root)) {
        const lhs = getAssignmentLhs(node);
        const rhs = getAssignmentRhs(node);
        if (!lhs || !rhs) continue;
        if (this.tainted.has(lhs)) continue;
        if (isSourceExpr(rhs) || this.expressionIsTainted(rhs)) {
          this.tainted.add(lhs);
          changed = true;
        }
      }
    }
  }
}

function getAssignmentLhs(node: Node): string | null {
  // Python: assignment, augmented_assignment
  // Java/C: assignment_expression
  if (node.type === "assignment" || node.type === "assignment_expression" || node.type === "augmented_assignment") {
    const left = node.childForFieldName("left");
    if (left?.type === "identifier") return left.text;
  }
  // Java: local_variable_declaration wraps variable_declarator
  if (node.type === "local_variable_declaration" || node.type === "variable_declarator") {
    const name = node.childForFieldName("name") ?? node.children.find(c => c.type === "identifier");
    if (name) return name.text;
  }
  // C: init_declarator (int x = expr)
  if (node.type === "init_declarator") {
    const decl = node.childForFieldName("declarator");
    if (decl?.type === "identifier") return decl.text;
  }
  return null;
}

function getAssignmentRhs(node: Node): Node | null {
  if (node.type === "assignment" || node.type === "assignment_expression" || node.type === "augmented_assignment") {
    return node.childForFieldName("right") ?? null;
  }
  if (node.type === "variable_declarator") {
    return node.childForFieldName("value") ?? null;
  }
  // C: init_declarator
  if (node.type === "init_declarator") {
    return node.childForFieldName("value") ?? null;
  }
  return null;
}

export function* walkAll(node: Node): Generator<Node> {
  yield node;
  for (const child of node.children) {
    yield* walkAll(child);
  }
}

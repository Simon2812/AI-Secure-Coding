"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaintTracker = void 0;
exports.walkAll = walkAll;
class TaintTracker {
    tainted = new Set();
    add(varName) {
        this.tainted.add(varName);
    }
    has(varName) {
        return this.tainted.has(varName);
    }
    expressionIsTainted(node) {
        return this.nodeContainsTaintedIdentifier(node);
    }
    nodeContainsTaintedIdentifier(node) {
        if (node.type === "identifier" && this.tainted.has(node.text)) {
            return true;
        }
        for (const child of node.children) {
            if (this.nodeContainsTaintedIdentifier(child))
                return true;
        }
        return false;
    }
    propagateAssignments(root, isSourceExpr) {
        let changed = true;
        while (changed) {
            changed = false;
            for (const node of walkAll(root)) {
                const lhs = getAssignmentLhs(node);
                const rhs = getAssignmentRhs(node);
                if (!lhs || !rhs)
                    continue;
                if (this.tainted.has(lhs))
                    continue;
                if (isSourceExpr(rhs) || this.expressionIsTainted(rhs)) {
                    this.tainted.add(lhs);
                    changed = true;
                }
            }
        }
    }
}
exports.TaintTracker = TaintTracker;
function getAssignmentLhs(node) {
    // Python: assignment, augmented_assignment
    // Java/C: assignment_expression
    if (node.type === "assignment" || node.type === "assignment_expression" || node.type === "augmented_assignment") {
        const left = node.childForFieldName("left");
        if (left?.type === "identifier")
            return left.text;
    }
    // Java: local_variable_declaration wraps variable_declarator
    if (node.type === "local_variable_declaration" || node.type === "variable_declarator") {
        const name = node.childForFieldName("name") ?? node.children.find(c => c.type === "identifier");
        if (name)
            return name.text;
    }
    // C: init_declarator (int x = expr)
    if (node.type === "init_declarator") {
        const decl = node.childForFieldName("declarator");
        if (decl?.type === "identifier")
            return decl.text;
    }
    return null;
}
function getAssignmentRhs(node) {
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
function* walkAll(node) {
    yield node;
    for (const child of node.children) {
        yield* walkAll(child);
    }
}
//# sourceMappingURL=taint.js.map
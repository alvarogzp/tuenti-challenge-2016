import java.lang.reflect.Array;
import java.util.Scanner;

class Challenge {
    private final Scanner in = new Scanner(System.in);

    public void solve() {
        int numberOfCases = in.nextInt();
        for (int c = 0; c < numberOfCases; c++) {
            solveCase(c + 1);
        }
    }

    private void solveCase(int caseNumber) {
        Case caseSolver = new Case(in);
        caseSolver.solve();
        String maxSum = getMaxSumString(caseSolver.getMaxSum());
        System.out.println("Case #" + caseNumber + ": " + maxSum);
    }

    private String getMaxSumString(int maxSum) {
        if (maxSum == Integer.MAX_VALUE) {
            return "INFINITY";
        } else {
            return String.valueOf(maxSum);
        }
    }

    public static void main(String[] args) {
        new Challenge().solve();
    }
}

class Case {
    private final Scanner in;

    private int lines;
    private int columns;

    private Matrix<Character> charMatrix;
    private Matrix<Integer> intMatrix;
    private Matrix<Integer> expandedIntMatrix;

    private int maxSum;

    public Case(Scanner in) {
        this.in = in;
    }

    public int getMaxSum() {
        return maxSum;
    }

    public void solve() {
        readCharMatrix();
        buildIntMatrixFromCharMatrix();
        expandIntMatrix();
        findMaxSum();
    }

    private void readCharMatrix() {
        lines = in.nextInt();
        columns = in.nextInt();
        charMatrix = Matrix.charMatrix(lines, columns);
        for (int l = 0; l < lines; l++) {
            String line = in.next();
            for (int c = 0; c < line.length(); c++) {
                char character = line.charAt(c);
                charMatrix.set(l, c, character);
            }
        }
    }

    private void buildIntMatrixFromCharMatrix() {
        intMatrix = Matrix.intMatrix(lines, columns);
        for (int l = 0; l < lines; l++) {
            for (int c = 0; c < columns; c++) {
                char character = charMatrix.get(l, c);
                intMatrix.set(l, c, mapCharToInt(character));
            }
        }
    }

    private int mapCharToInt(char character) {
        if (character >= 65 && character <= 90) { // A-Z
            return character - 64; // positive number
        } else if (character >= 97 && character <= 122) { // a-z
            return (character - 96) * -1; // negative number
        } else if (character == '.') {
            return 0;
        } else {
            throw new RuntimeException("invalid char: " + character);
        }
    }

    private void expandIntMatrix() {
        MatrixExpander matrixExpander = new MatrixExpander(intMatrix);
        matrixExpander.expand();
        expandedIntMatrix = matrixExpander.getExpandedMatrix();
    }

    private void findMaxSum() {
        maxSum = new MaxSumCalculator(expandedIntMatrix).findMaxSum();
    }
}

class Matrix<T> {
    public final T[][] matrix;
    public final int lines;
    public final int columns;

    public Matrix(T[][] matrix, int lines, int columns) {
        this.matrix = matrix;
        this.lines = lines;
        this.columns = columns;
    }

    public Matrix(Class<T> type, int lines, int columns) {
        this.matrix = (T[][]) Array.newInstance(type, lines, columns);
        this.lines = lines;
        this.columns = columns;
    }

    public static Matrix<Integer> intMatrix(int lines, int columns) {
        return new Matrix<>(Integer.class, lines, columns);
    }

    public static Matrix<Character> charMatrix(int lines, int columns) {
        return new Matrix<>(Character.class, lines, columns);
    }

    public T get(int line, int column) {
        return matrix[line][column];
    }

    public T[] get(int line) {
        return matrix[line];
    }

    public void set(int line, int column, T value) {
        matrix[line][column] = value;
    }

    public void set(int line, T[] value) {
        matrix[line] = value;
    }
}

class MatrixExpander {
    private final Matrix<Integer> originalMatrix;
    private final int originalLines;
    private final int originalColumns;

    private Matrix<Integer> expandedMatrix;
    private int expandedLines;
    private int expandedColumns;

    private int offsetLines;
    private int offsetColumns;

    public MatrixExpander(Matrix<Integer> matrix) {
        this.originalMatrix = matrix;
        originalLines = matrix.lines;
        originalColumns = matrix.columns;
    }

    public Matrix<Integer> getExpandedMatrix() {
        return expandedMatrix;
    }

    public void expand() {
        expandedLines = getExpandedDimensionFromOriginal(originalLines);
        expandedColumns = getExpandedDimensionFromOriginal(originalColumns);
        expandedMatrix = Matrix.intMatrix(expandedLines, expandedColumns);
        offsetLines = getOffset(originalLines, expandedLines);
        offsetColumns = getOffset(originalColumns, expandedColumns);
        expandColumns();
        expandLines();
    }

    private int getExpandedDimensionFromOriginal(int original) {
        if (original % 2 == 0) { // even
            return original * 2;
        } else { // odd
            return original * 2 - 1;
        }
    }

    private int getOffset(int original, int expanded) {
        return (expanded - original) / 2;
    }

    private void expandColumns() {
        // first stage, lines are not expanded yet
        int startLine = offsetLines;
        int endLine = expandedLines - offsetLines;
        for (int column = 0; column < expandedColumns; column++) {
            int columnToCopy = getIndexToCopy(column, offsetColumns, originalColumns);
            for (int line = startLine; line < endLine; line++) {
                int value = originalMatrix.get(line - offsetLines, columnToCopy);
                expandedMatrix.set(line, column, value);
            }
        }
    }

    private void expandLines() {
        // second stage, columns are already expanded
        for (int line = 0; line < expandedLines; line++) {
            int lineToCopy = getIndexToCopy(line, offsetLines, originalLines);
            Integer[] matrixLine = expandedMatrix.get(lineToCopy + offsetLines);
            expandedMatrix.set(line, matrixLine);
        }
    }

    private int getIndexToCopy(int currentIndex, int offset, int originalLength) {
        int normalizedIndex = currentIndex - offset;
        if (normalizedIndex >= 0 && normalizedIndex < originalLength) {
            return normalizedIndex; // copy same index
        } else if (normalizedIndex >= originalLength) {
            return normalizedIndex - originalLength; // copy from start
        } else { // currentIndex < 0
            return originalLength + normalizedIndex;
        }
    }
}

class MaxSumCalculator {
    private final Matrix<Integer> matrix;

    MaxSumCalculator(Matrix<Integer> matrix) {
        this.matrix = matrix;
    }

    public int findMaxSum() {
        if (allNumbersArePositive()) {
            return Integer.MAX_VALUE;
        } else if (allNumbersAreNegative()) {
            return 0;
        } else {
            return findMaxSumUsingKandaneAlgorithm(matrix.matrix, matrix.lines, matrix.columns);
        }
    }

    private boolean allNumbersArePositive() {
        for (int l = 0; l < matrix.lines; l++) {
            for (int c = 0; c < matrix.columns; c++) {
                if (matrix.get(l, c) <= 0) {
                    return false;
                }
            }
        }
        return true;
    }

    private boolean allNumbersAreNegative() {
        for (int l = 0; l < matrix.lines; l++) {
            for (int c = 0; c < matrix.columns; c++) {
                if (matrix.get(l, c) >= 0) {
                    return false;
                }
            }
        }
        return true;
    }

    // copied from http://stackoverflow.com/a/5123959/5373629
    private int findMaxSumUsingKandaneAlgorithm(Integer[][] matrix, int lines, int columns) {
        //computing the vertical prefix sum for columns
        int[][] ps = new int[lines][columns];
        for (int i = 0; i < columns; i++) {
            for (int j = 0; j < lines; j++) {
                if (j == 0) {
                    ps[j][i] = matrix[j][i];
                } else {
                    ps[j][i] = matrix[j][i] + ps[j - 1][i];
                }
            }
        }

        int maxSum = matrix[0][0];

        //Auxiliary variables
        int[] sum = new int[columns];
        int[] pos = new int[columns];
        int localMax;

        for (int i = 0; i < lines; i++) {
            for (int k = i; k < lines; k++) {
                // Kandane over all columns with the i..k rows
                reset(sum);
                reset(pos);
                localMax = 0;
                //we keep track of the position of the max value over each Kandane's execution
                // notice that we do not keep track of the max value, but only its position
                sum[0] = ps[k][0] - (i == 0 ? 0 : ps[i - 1][0]);
                for (int j = 1; j < columns; j++) {
                    if (sum[j - 1] > 0) {
                        sum[j] = sum[j - 1] + ps[k][j] - (i == 0 ? 0 : ps[i - 1][j]);
                        pos[j] = pos[j - 1];
                    } else {
                        sum[j] = ps[k][j] - (i == 0 ? 0 : ps[i - 1][j]);
                        pos[j] = j;
                    }
                    if (sum[j] > sum[localMax]) {
                        localMax = j;
                    }
                }//Kandane ends here

                if (sum[localMax] > maxSum) {
                  /* sum[localMax] is the new max value
                    the corresponding submatrix goes from rows i..k.
                     and from columns pos[localMax]..localMax
                     */
                    maxSum = sum[localMax];
                }
            }
        }

        return maxSum;
    }

    private void reset(int[] a) {
        for (int index = 0; index < a.length; index++) {
            a[index] = 0;
        }
    }
}

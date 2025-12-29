# Epoxy Composite Design

## Multi-Output Learning: Regressor Chains

<table>
  <thead>
    <tr>
      <th>Step</th>
      <th>Input Data</th>
      <th>Predicted Target(s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Base Features</td>
      <td>Tensile Strength</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Base Features + Tensile Strength</td>
      <td>Flexural Strength</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Base Features + Tensile Strength + Flexural Strength</td>
      <td>Elongation at Break<br>Impact Strength</td>
    </tr>
  </tbody>
</table>

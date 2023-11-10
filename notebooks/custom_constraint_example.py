
from sdv.constraints import create_custom_constraint_class

## COPIED FROM ABOVE
def is_valid(column_names, data):
  # let's assume the first column name is the boolean column (has_rewards)
  # and the second column is the numerical column (amenities_fee)
  boolean_column = column_names[0]
  numerical_column = column_names[1]

  # if the first column is True, the second must be 0
  true_values = (data[boolean_column] == True) & (data[numerical_column] == 0.0)
  
  # if the first is False, then the second can be anything
  false_values = (data[boolean_column] == False)

  return (true_values) | (false_values)

def transform(column_names, data):
  # let's assume the first column name is the boolean column (has_rewards)
  # and the second column is the numerical column (amenities_fee)
  boolean_column = column_names[0]
  numerical_column = column_names[1]

  # let's replace the 0 values with a typical value (median)
  typical_value = data[numerical_column].median()
  data[numerical_column] = data[numerical_column].mask(data[boolean_column] == True, typical_value)
  
  return data

def reverse_transform(column_names, data):
  # let's assume the first column name is the boolean column (has_rewards)
  # and the second column is the numerical column (amenities_fee)
  boolean_column = column_names[0]
  numerical_column = column_names[1]

  # set the numerical column to 0 if the boolean is True
  data[numerical_column] = data[numerical_column].mask(data[boolean_column] == True, 0.0)
  
  return data

IfTrueThenZero = create_custom_constraint_class(
    is_valid_fn=is_valid,
    transform_fn=transform,
    reverse_transform_fn=reverse_transform
)

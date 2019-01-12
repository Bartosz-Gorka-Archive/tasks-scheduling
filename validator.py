class Validator():
    n = None
    k = None
    h = None

    def are_valid_parameters(self, args):
        return self.validate_arguments(args) and \
               self.validate_file_name(args[1]) and \
               self.validate_instance_no(args[2]) and \
               self.validate_param_h(args[3])

    def parameters(self):
        return self.n, self.k, self.h

    def validate_file_name(self, number):
        self.n = int(number)
        correct_file_numbers = ['10', '20', '50', '100', '200', '500', '1000']
        return number in correct_file_numbers

    @staticmethod
    def validate_arguments(args):
        return len(args) >= 4

    def validate_instance_no(self, instance_number):
        self.k = int(instance_number)
        return instance_number in [str(i) for i in list(range(1, 11))]

    def validate_param_h(self, h):
        self.h = float(h)
        return h in ['0.2', '0.4', '0.6', '0.8']

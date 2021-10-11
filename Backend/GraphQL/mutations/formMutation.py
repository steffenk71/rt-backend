

#from Backend.database import access_secret_version, db
#from Backend.DataTypes.User import User
from Backend.Authentication.verify_token import get_user_context
from Backend.DataTypes.Exceptions.AuthenticationException import AuthenticationException
from Backend.DataTypes.Exceptions.IncorrectParameterException import IncorrectParameterException
from Backend.emails import Emails
from Backend.DataTypes.Status import Status
from Backend.GraphQL.shared import  mutation, get_applicant_document
from Backend.GraphQL.mutations.emailMutation import config_track
@mutation.field("saveForm")
def save_form(_, info,  applicant_id, batch_id, location, streetNumber, addressSuffix, postcode, city, country, accountHolder, bankName, iban, bic, shirtSize, shirtStyle, foodIntolerances):
        try:
            application, application_details = get_applicant_document(info, batch_id, applicant_id)
        except Exception as err:
            return IncorrectParameterException(errorMessage=err.__str__())

        if(application):
            acceptanceFormData = { 
                        'location': location,
                        'streetNumber': streetNumber,
                        'addressSuffix': addressSuffix,
                        'postcode':  postcode,
                        'city': city,
                        'country': country,
                        'accountHolder': accountHolder,
                        'bankName': bankName,
                        'iban': iban,
                        'bic': bic,
                        'shirtSize': shirtSize,
                        'shirtStyle': shirtStyle,
                        'foodIntolerances': foodIntolerances
            }
            application.set({"acceptanceFormData": acceptanceFormData}, merge=True)
            track_class = config_track(application_details['track'])
            Emails('sendFormConfirmation', applicant_id, application_details['name'], application_details['email'], track_class, batch_id, acceptanceFormData).send_email()
            Emails('sendDocuments', applicant_id, application_details['name'], application_details['email'], track_class, batch_id, acceptanceFormData).send_email_with_attach()
            return Status(0,'Form was succesfully saved')

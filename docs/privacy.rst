Privacy
========

Anonymization
-------------

User privacy is important, not only to meet local regulations, but also to
protect your users and allow them to exercise their rights. However,
it's not always practical to delete users, especially if they have dependent
objects, that are relevant for statistical analysis.

Anonymization is a process of removing the user's personal data whilst keeping
related data intact. This is done by using the ``anomymize`` method.



.. automethod:: mailauth.contrib.user.models.AbstractEmailUser.anonymize
    :noindex:

This method may be overwritten to provide anonymization for you custom user model.

Related objects may also listen to the anonymize signal.

.. autoclass:: mailauth.contrib.user.signals.anonymize

All those methods can be conveniently triggered via the ``anonymize`` admin action.

.. autoclass:: mailauth.contrib.user.admin.AnonymizableAdminMixin
    :members:

Liability Waiver
----------------

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

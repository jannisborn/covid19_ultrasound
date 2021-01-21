import React from 'react';
import {Route, Switch, useHistory, useLocation} from 'react-router-dom';
import Layout from '../Layout';
import {Helmet} from 'react-helmet';
import configuration from '../../utils/constants';

const Terms = () => {

    return (
        <Layout>
            <Helmet>
                <title>{configuration.appTitle} - Terms and conditions</title>
            </Helmet>
            <div className="spacer-small">
                <div className="container">
                    <div className="text row mb-5">
                        <div className="col-lg-10 offset-lg-1 terms">
                            <header>
                                <h2 className="mb-4">Terms and conditions</h2>
                            </header>
                            <div className="terms-spacer">
                                <p>PLEASE READ THESE TERMS AND CONDITIONS ("TERMS", "TERMS AND CONDITIONS") CAREFULLY
                                    BEFORE USING THE <a
                                        href="https://pocovidscreen.org/">HTTPS://POCOVIDSCREEN.ORG/</a> WEBSITE (THE
                                    "SERVICE") OPERATED BY POCOVIDSCREEN ("US", "WE", OR "OUR").
                                </p>
                                <p>
                                    YOUR ACCESS TO AND USE OF THE SERVICE IS CONDITIONED UPON YOUR ACCEPTANCE OF AND
                                    COMPLIANCE WITH THESE TERMS. THESE TERMS APPLY TO ALL VISITORS, USERS AND OTHERS WHO
                                    WISH TO ACCESS OR USE THE SERVICE. BY ACCESSING OR USING THE SERVICE YOU AGREE TO BE
                                    BOUND BY THESE TERMS. IF YOU DISAGREE WITH ANY PART OF THE TERMS THEN YOU DO NOT
                                    HAVE PERMISSION TO ACCESS THE SERVICE.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Communications</h3>
                                <p>By creating an Account on our service, you agree to subscribe to newsletters,
                                    marketing or promotional materials and other information we may send. However, you
                                    may opt out of receiving any, or all, of these communications from us by following
                                    the unsubscribe link or instructions provided in any email we send.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Content</h3>
                                <p>Our Service allows you to post, link, store, share and otherwise make available
                                    certain information graphics, videos, or other material ("Content"). You are
                                    responsible for the Content that you post on or through the Service, including its
                                    legality, reliability, and appropriateness.</p>
                                <p>By posting Content on or through the Service, You represent and warrant that: (i) the
                                    Content is yours (you own it) and/or you have the right to use it and the right to
                                    grant us the rights and license as provided in these Terms, and (ii) that the
                                    posting of your Content on or through the Service does not violate the privacy
                                    rights, publicity rights, copyrights, contract rights or any other rights of any
                                    person or entity. We reserve the right to terminate the account of anyone found to
                                    be infringing on a copyright.
                                </p>
                                <p>You retain any and all of your rights to any Content you submit, post or display on
                                    or through the Service and you are responsible for protecting those rights. We take
                                    no responsibility and assume no liability for Content you or any third party posts
                                    on or through the Service. However, by posting Content using the Service you grant
                                    us the right and license to use, modify, perform, display, reproduce, and distribute
                                    such Content on and through the Service.
                                </p>
                                <p>Pocovidscreen has the right but not the obligation to monitor and edit all Content
                                    provided by users. In addition, Content found on or through this Service are the
                                    property of Pocovidscreen or used with permission. You may not distribute, modify,
                                    transmit, reuse, download, repost, copy, or use said Content, whether in whole or in
                                    part, for commercial purposes or for personal gain, without express advance written
                                    permission from us.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Accounts</h3>
                                <p>When you create an account with us, you guarantee that you are above the age of 18,
                                    and that the information you provide us is accurate, complete, and current at all
                                    times. Inaccurate, incomplete, or obsolete information may result in the immediate
                                    termination of your account on the Service.</p>
                                <p>You are responsible for maintaining the confidentiality of your account and password,
                                    including but not limited to the restriction of access to your computer and/or
                                    account. You agree to accept responsibility for any and all activities or actions
                                    that occur under your account and/or password, whether your password is with our
                                    Service or a third-party service. You must notify us immediately upon becoming aware
                                    of any breach of security or unauthorized use of your account.
                                </p>
                                <p>You may not use as a username the name of another person or entity or that is not
                                    lawfully available for use, a name or trademark that is subject to any rights of
                                    another person or entity other than you, without appropriate authorization. You may
                                    not use as a username any name that is offensive, vulgar or obscene.
                                </p>
                                <p>You may only use an institution name (in the field of Institution) if you have
                                    permission to do so and if you are by any means affiliated to it or with a working
                                    contract that can prove the working relationship.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Copyright Policy</h3>
                                <p>We respect the intellectual property rights of others. It is our policy to respond to
                                    any claim that Content posted on the Service infringes on the copyright or other
                                    intellectual property rights ("Infringement") of any person or entity.</p>
                                <p>If you are a copyright owner, or authorized on behalf of one, and you believe that
                                    the copyrighted work has been copied in a way that constitutes copyright
                                    infringement, please submit your claim via email to pocovidaccount@gmail.com, with
                                    the subject line: "Copyright Infringement" and include in your claim a detailed
                                    description of the alleged Infringement as detailed below, under "DMCA Notice and
                                    Procedure for Copyright Infringement Claims".
                                </p>
                                <p>You may be held accountable for damages (including costs and attorneys' fees) for
                                    misrepresentation or bad-faith claims on the infringement of any Content found on
                                    and/or through the Service on your copyright.
                                </p>
                                <p><strong>EUROPEAN ENTITY Notice and Procedure for Copyright Infringement
                                    Claims</strong></p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Intellectual Property</h3>
                                <p>The Service and its original content (excluding Content provided by users), features
                                    and functionality are and will remain the exclusive property of Pocovidscreen and
                                    its licensors. The Service is protected by copyright, trademark, and other laws of
                                    the European Union and Associated Territory. Our trademarks and trade dress may not
                                    be used in connection with any product or service without the prior written consent
                                    of Pocovidscreen.</p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Intellectual Property</h3>
                                <p>Our Service may contain links to third party web sites or services that are not owned
                                    or controlled by Pocovidscreen. Pocovidscreen has no control over, and assumes no
                                    responsibility for the content, privacy policies, or practices of any third party
                                    web sites or services. We do not warrant the offerings of any of these
                                    entities/individuals or their websites. You acknowledge and agree that Pocovidscreen
                                    shall not be responsible or liable, directly or indirectly, for any damage or loss
                                    caused or alleged to be caused by or in connection with use of or reliance on any
                                    such content, goods or services available on or through any such third party web
                                    sites or services. We strongly advise you to read the terms and conditions and
                                    privacy policies of any third party web sites or services that you visit.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Termination</h3>
                                <p>We may terminate or suspend your account and bar access to the Service immediately,
                                    without prior notice or liability, under our sole discretion, for any reason
                                    whatsoever and without limitation, including but not limited to a breach of the
                                    Terms.
                                </p>
                                <p>If you wish to terminate your account, you may simply discontinue using the Service.
                                    All provisions of the Terms which by their nature should survive termination shall
                                    survive termination, including, without limitation, ownership provisions, warranty
                                    disclaimers, indemnity and limitations of liability.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Indemnification</h3>
                                <p>You agree to defend, indemnify and hold harmless Pocovidscreen and its licensee and
                                    licensors, and their employees, contractors, agents, officers and directors, from
                                    and against any and all claims, damages, obligations, losses, liabilities, costs or
                                    debt, and expenses (including but not limited to attorney's fees), resulting from or
                                    arising out of a) your use and access of the Service, by you or any person using
                                    your account and password; b) a breach of these Terms, or c) Content posted on the
                                    Service.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Limitation Of Liability</h3>
                                <p>In no event shall Pocovidscreen, nor its directors, employees, partners, agents,
                                    suppliers, or affiliates, be liable for any indirect, incidental, special,
                                    consequential or punitive damages, including without limitation, loss of profits,
                                    data, use, goodwill, or other intangible losses, resulting from (i) your access to
                                    or use of or inability to access or use the Service; (ii) any conduct or content of
                                    any third party on the Service; (iii) any content obtained from the Service; and
                                    (iv) unauthorized access, use or alteration of your transmissions or content,
                                    whether based on warranty, contract, tort (including negligence) or any other legal
                                    theory, whether or not we have been informed of the possibility of such damage, and
                                    even if a remedy set forth herein is found to have failed of its essential purpose.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Disclaimer</h3>
                                <p>Your use of the Service is at your sole risk. The Service is provided on an "AS IS"
                                    and "AS AVAILABLE" basis. The Service is provided without warranties of any kind,
                                    whether express or implied, including, but not limited to, implied warranties of
                                    merchantability, fitness for a particular purpose, non-infringement or course of
                                    performance.
                                </p>
                                <p>Pocovidscreen its subsidiaries, affiliates, and its licensors do not warrant that a)
                                    the Service will function uninterrupted, secure or available at any particular time
                                    or location; b) any errors or defects will be corrected; c) the Service is free of
                                    viruses or other harmful components; or d) the results of using the Service will
                                    meet your requirements.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Exclusions</h3>
                                <p>Some jurisdictions do not allow the exclusion of certain warranties or the exclusion
                                    or limitation of liability for consequential or incidental damages, so the
                                    limitations above may not apply to you.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Governing Law</h3>
                                <p>These Terms shall be governed and construed in accordance with the laws of European
                                    Union and Associated Territories, without regard to its conflict of law provisions.
                                </p>
                                <p>
                                    Our failure to enforce any right or provision of these Terms will not be considered
                                    a waiver of those rights. If any provision of these Terms is held to be invalid or
                                    unenforceable by a court, the remaining provisions of these Terms will remain in
                                    effect. These Terms constitute the entire agreement between us regarding our
                                    Service, and supersede and replace any prior agreements we might have had between us
                                    regarding the Service.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Changes</h3>
                                <p>We reserve the right, at our sole discretion, to modify or replace these Terms at any
                                    time. If a revision is material we will provide at least 30 days notice prior to any
                                    new terms taking effect. What constitutes a material change will be determined at
                                    our sole discretion.
                                </p>
                                <p>
                                    By continuing to access or use our Service after any revisions become effective, you
                                    agree to be bound by the revised terms. If you do not agree to the new terms, you
                                    are no longer authorized to use the Service.
                                </p>
                            </div>
                            <div className="terms-spacer">
                                <h3>Contact us</h3>
                                <p>If you have any questions about these Terms, please contact us at <a
                                    href="mailto:info@pocovidscreen.org"
                                    title="Get in touch by email">info@pocovidscreen.org</a>.
                                </p>
                                <p>
                                    By continuing to access or use our Service after any revisions become effective, you
                                    agree to be bound by the revised terms. If you do not agree to the new terms, you
                                    are no longer authorized to use the Service.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Terms;
